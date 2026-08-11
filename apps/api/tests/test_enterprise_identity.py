import sys
import asyncio
from pathlib import Path

api_dir = Path(__file__).resolve().parent.parent
if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.identity import SCIMUserCreate, SCIMUserEmail, ServiceAccountCreate
from app.services import identity_service

client = TestClient(app)

def test_oidc_validation_and_replay_defense():
    async def _test():
        provider_id = "idp_oidc_01"

        # 1. Valid OIDC claims -> SUCCESS
        valid_claims = {
            "iss": "https://company.okta.com",
            "aud": "vapor_app",
            "exp": 253402300800,  # Year 9999
            "sub": "okta_sub_1042",
            "email": "executive@company.com",
            "email_verified": True,
            "nonce": "nonce_xyz123"
        }
        res, err = await identity_service.authenticate_oidc(None, provider_id, valid_claims, nonce="nonce_xyz123")
        assert err is None
        assert res["email"] == "executive@company.com"

        # 2. Expired Token -> REJECTED
        expired_claims = dict(valid_claims, exp=1000000000)
        res_exp, err_exp = await identity_service.authenticate_oidc(None, provider_id, expired_claims)
        assert err_exp == "OIDC Token Expired"

        # 3. Nonce Mismatch -> REJECTED
        res_nonce, err_nonce = await identity_service.authenticate_oidc(None, provider_id, valid_claims, nonce="wrong_nonce")
        assert "OIDC Nonce Mismatch" in err_nonce

    asyncio.run(_test())

def test_saml_assertion_validation_and_replay_protection():
    async def _test():
        provider_id = "idp_saml_01"
        assertion_id = "saml_assertion_unique_987"

        valid_assertion = {
            "assertion_id": assertion_id,
            "issuer": "https://login.microsoftonline.com/saml2",
            "audience": "https://vapor.app/saml",
            "not_on_or_after": 253402300800,
            "subject_email": "saml.user@company.com",
            "signature_valid": True
        }

        # 1. Valid SAML Assertion -> SUCCESS
        res, err = await identity_service.authenticate_saml(None, provider_id, valid_assertion)
        assert err is None
        assert res["email"] == "saml.user@company.com"

        # 2. Replayed Assertion -> REJECTED BY REPLAY PROTECTION
        res_rep, err_rep = await identity_service.authenticate_saml(None, provider_id, valid_assertion)
        assert "SAML Replay Attack Detected" in err_rep

    asyncio.run(_test())

def test_jit_user_provisioning_default_role():
    async def _test():
        org_id = "org_jit_test"
        auth_data = {
            "email": "new.employee@company.com",
            "name": "New Employee",
            "email_verified": True
        }

        # JIT user gets default 'member' role (never admin)
        user = await identity_service.provision_jit_user(None, org_id, auth_data)
        assert user["role"] == "member"
        assert user["email"] == "new.employee@company.com"

    asyncio.run(_test())

def test_scim_user_lifecycle_and_deprovisioning():
    async def _test():
        org_id = "org_scim_test"
        scim_in = SCIMUserCreate(
            userName="scim.user@company.com",
            emails=[SCIMUserEmail(value="scim.user@company.com")],
            active=True
        )

        # 1. Create User
        scim_user = await identity_service.scim_create_user(None, org_id, scim_in)
        assert scim_user["active"] is True

        # 2. Deprovision User (active=false) -> Revokes sessions and pauses automations
        dep_res = await identity_service.scim_deprovision_user(None, org_id, scim_user["id"])
        assert dep_res["active"] is False
        assert dep_res["offboard_status"]["status"] == "offboarded"

    asyncio.run(_test())

def test_service_account_token_hashing():
    async def _test():
        org_id = "org_sa_test"
        sa_in = ServiceAccountCreate(
            organizationId=org_id,
            name="CI/CD Pipeline Service",
            scopes=["workflow.run", "workspace.read"]
        )

        sa_dict, raw_token = await identity_service.create_service_account(None, sa_in, "usr_admin_01")
        assert raw_token.startswith("vpr_sa_")
        assert sa_dict["name"] == "CI/CD Pipeline Service"

    asyncio.run(_test())

def test_identity_and_scim_rest_api():
    headers = {"Authorization": "Bearer scim_secret_token_123"}

    # 1. IdP Providers API
    idp_res = client.get("/api/v1/admin/identity/providers?organizationId=org_default_creator")
    assert idp_res.status_code == 200
    assert len(idp_res.json()) >= 2

    # 2. Test Connection API
    test_res = client.post("/api/v1/admin/identity/providers/idp_oidc_01/test")
    assert test_res.status_code == 200
    assert test_res.json()["status"] == "SUCCESS"

    # 3. Verified Domains API
    dom_res = client.get("/api/v1/admin/identity/domains?organizationId=org_default_creator")
    assert dom_res.status_code == 200

    # 4. Service Accounts API
    sa_res = client.get("/api/v1/admin/identity/service-accounts?organizationId=org_default_creator")
    assert sa_res.status_code == 200

    # 5. SCIM Users API
    scim_u_res = client.get("/scim/v2/Users", headers=headers)
    assert scim_u_res.status_code == 200
    assert len(scim_u_res.json()["Resources"]) >= 1

    # 6. SCIM Groups API
    scim_g_res = client.get("/scim/v2/Groups", headers=headers)
    assert scim_g_res.status_code == 200
