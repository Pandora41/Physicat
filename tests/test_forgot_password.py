from app import create_app, db
from app.config import Settings
from app.models import User


def test_forgot_password_flow_allows_reset(monkeypatch):
    test_settings = Settings(
        flask_env="testing",
        flask_debug=True,
        database_url="sqlite:///:memory:",
        secret_key="test-secret-key",
    )
    app = create_app(test_settings)

    with app.app_context():
        db.create_all()
        user = User(username="resetter", email="reset@example.com")
        user.set_password("oldpassword")
        user.is_verified = True
        db.session.add(user)
        db.session.commit()

        from app.routes import pages

        sent_tokens = []

        def fake_send_reset_email(recipient, token):
            sent_tokens.append((recipient, token))

        monkeypatch.setattr(pages, "send_password_reset_email", fake_send_reset_email)

        with app.test_client() as client:
            response = client.post(
                "/forgot-password",
                data={"email": "reset@example.com"},
                follow_redirects=True,
            )

            assert response.status_code == 200
            assert len(sent_tokens) == 1
            assert sent_tokens[0][0] == "reset@example.com"

            token = sent_tokens[0][1]

            reset_page = client.get(f"/reset-password/{token}")
            assert reset_page.status_code == 200

            reset_response = client.post(
                f"/reset-password/{token}",
                data={"password": "newpassword123", "confirm_password": "newpassword123"},
                follow_redirects=True,
            )

            assert reset_response.status_code == 200

            refreshed_user = User.query.filter_by(email="reset@example.com").first()
            assert refreshed_user is not None
            assert refreshed_user.check_password("newpassword123")
            assert not refreshed_user.check_password("oldpassword")

        db.drop_all()
