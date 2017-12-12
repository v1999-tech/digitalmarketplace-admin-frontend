import mock
import pytest
from lxml import html

from ...helpers import LoggedInApplicationTest


class TestIndex(LoggedInApplicationTest):
    @mock.patch('app.main.views.services.data_api_client')
    def test_index_shows_frameworks_in_standstill_or_live(self, data_api_client):
        self.user_role = 'admin-ccs-sourcing'
        data_api_client.find_frameworks.return_value = {'frameworks': [
            {'id': 1, 'frameworkAgreementVersion': None, 'name': 'Framework 1', 'slug': 'framework-1',
             'status': 'standstill'},
            {'id': 2, 'frameworkAgreementVersion': 'v1.0', 'name': 'Framework 2', 'slug': 'framework-2',
             'status': 'live'},
            {'id': 3, 'frameworkAgreementVersion': None, 'name': 'Framework 3', 'slug': 'framework-3',
             'status': 'open'},
        ]}

        response = self.client.get('/admin')
        data = response.get_data(as_text=True)

        assert 'Download Framework 1 agreements' in data
        assert 'Approve Framework 2 agreements for countersigning' in data

        # Agreements should be in reverse-chronological order.
        assert (
            data.index('Approve Framework 2 agreements for countersigning') <
            data.index('Download Framework 1 agreements')
        )

        # Only standstill/live agreements should be listed.
        assert 'Download Framework 3 agreements' not in data

    @pytest.mark.parametrize("role, link_should_be_visible", [
        ("admin", True),
        ("admin-ccs-category", False),
        ("admin-ccs-sourcing", False),
        ("admin-framework-manager", False),
        ("admin-manager", False),
    ])
    def test_add_buyer_email_domain_link_is_shown_to_users_with_right_roles(self, role, link_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        link_is_visible = bool(document.xpath('.//a[@href="/admin/buyers/add-buyer-domains"]'))

        assert link_is_visible is link_should_be_visible, (
            "Role {} {} see the link".format(role, "can not" if link_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, header_should_be_visible", [
        ("admin", True),
        ("admin-ccs-category", True),
        ("admin-ccs-sourcing", False),
        ("admin-framework-manager", False),
        ("admin-manager", False),
    ])
    def test_user_support_header_is_shown_to_users_with_right_roles(self, role, header_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        header_is_visible = bool(document.xpath('.//h1[contains(text(),"User support")]'))

        assert header_is_visible is header_should_be_visible, (
            "Role {} {} see the header".format(role, "can not" if header_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, link_should_be_visible", [
        ("admin", True),
        ("admin-ccs-category", True),
        ("admin-ccs-sourcing", False),
        ("admin-framework-manager", False),
        ("admin-manager", False),
    ])
    def test_find_a_user_by_email_link_is_shown_to_users_with_right_roles(self, role, link_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        link_is_visible = bool(document.xpath('.//a[@href="/admin/users"]'))

        assert link_is_visible is link_should_be_visible, (
            "Role {} {} see the link".format(role, "can not" if link_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, link_should_be_visible", [
        ("admin", False),
        ("admin-ccs-category", False),
        ("admin-ccs-sourcing", False),
        ("admin-framework-manager", False),
        ("admin-manager", True),
    ])
    def test_manage_admin_users_link_is_shown_to_users_with_the_right_role(self, role, link_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        link_is_visible = bool(document.xpath('.//a[@href="/admin/admin-users"]'))

        assert link_is_visible is link_should_be_visible, (
            "Role {} {} see the link".format(role, "can not" if link_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, link_should_be_visible", [
        ("admin", False),
        ("admin-ccs-category", True),
        ("admin-ccs-sourcing", False),
        ("admin-framework-manager", False),
        ("admin-manager", False),
    ])
    def test_check_service_edits_link_is_shown_to_users_with_the_right_role(self, role, link_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        link_is_visible = bool(document.xpath('.//a[@href="/admin/services/updates/unapproved"]'))

        assert link_is_visible is link_should_be_visible, (
            "Role {} {} see the link".format(role, "can not" if link_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, header_should_be_visible", [
        ("admin", False),
        ("admin-ccs-category", False),
        ("admin-ccs-sourcing", True),
        ("admin-framework-manager", True),
        ("admin-manager", False),
    ])
    def test_statistics_header_is_shown_to_users_with_the_right_role(self, role, header_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        header_is_visible = bool(document.xpath('.//h1[contains(text(),"Statistics")]'))

        assert header_is_visible is header_should_be_visible, (
            "Role {} {} see the header".format(role, "can not" if header_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, header_should_be_visible", [
        ("admin", False),
        ("admin-ccs-category", True),
        ("admin-ccs-sourcing", True),
        ("admin-framework-manager", True),
        ("admin-manager", False),
    ])
    def test_view_agreements_links_are_shown_to_users_with_the_right_role(self, role, header_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        header_is_visible = bool(document.xpath('.//h1[contains(text(),"Agreements")]'))

        assert header_is_visible is header_should_be_visible, (
            "Role {} {} see the header".format(role, "can not" if header_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, header_should_be_visible", [
        ("admin", False),
        ("admin-ccs-category", False),
        ("admin-ccs-sourcing", False),
        ("admin-framework-manager", True),
        ("admin-manager", False),
    ])
    def test_view_communications_links_are_shown_to_users_with_the_right_role(self, role, header_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        header_is_visible = bool(document.xpath('.//h1[contains(text(),"Communications")]'))

        assert header_is_visible is header_should_be_visible, (
            "Role {} {} see the header".format(role, "can not" if header_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, link_should_be_visible", [
        ("admin", False),
        ("admin-ccs-category", False),
        ("admin-ccs-sourcing", False),
        ("admin-framework-manager", True),
        ("admin-manager", False),
    ])
    def test_download_user_lists_link_is_shown_to_users_with_the_right_role(self, role, link_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        link_is_visible = bool(document.xpath('.//a[@href="/admin/users/download"]'))

        assert link_is_visible is link_should_be_visible, (
            "Role {} {} see the link".format(role, "can not" if link_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, link_should_be_visible", [
        ("admin", True),
        ("admin-ccs-category", True),
        ("admin-ccs-sourcing", False),
        ("admin-framework-manager", False),
        ("admin-manager", False),
    ])
    def test_find_buyer_by_opportunity_id_link_is_shown_to_users_with_right_roles(self, role, link_should_be_visible):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        link_is_visible = bool(document.xpath('.//a[@href="/admin/buyers"]'))

        assert link_is_visible is link_should_be_visible, (
            "Role {} {} see the link".format(role, "can not" if link_should_be_visible else "can")
        )

    @pytest.mark.parametrize("role, link_should_be_visible, expected_link_text", [
        ("admin", True, "Edit supplier accounts or view services"),
        ("admin-ccs-category", True, "Edit suppliers and services"),
        ("admin-ccs-sourcing", True, "Edit supplier declarations"),
        ("admin-framework-manager", True, "View suppliers and services"),
        ("admin-manager", False, None),
    ])
    def test_link_to_find_suppliers_and_services_page_is_shown_with_role_dependent_text(
            self, role, link_should_be_visible, expected_link_text
    ):
        self.user_role = role
        response = self.client.get('/admin')
        document = html.fromstring(response.get_data(as_text=True))
        link_is_visible = bool(document.xpath('.//a[@href="/admin/find-suppliers-and-services"]'))

        assert link_is_visible is link_should_be_visible, (
            "Role {} {} see the link".format(role, "can not" if link_should_be_visible else "can")
        )
        if link_should_be_visible:
            link_text = document.xpath('.//a[@href="/admin/find-suppliers-and-services"]//text()')[0]
            assert link_text == expected_link_text