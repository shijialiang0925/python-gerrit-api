#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from gerrit.utils.models import BaseModel
from gerrit.accounts.account import GerritAccount
from gerrit.utils.common import check


class GerritGroup(BaseModel):
    def __init__(self, **kwargs):
        super(GerritGroup, self).__init__(**kwargs)
        self.attributes = ['name', 'url', 'options', 'description',
                           'id', 'group_id', 'owner', 'owner_id', 'created_on', 'gerrit']

    @check
    def rename(self, input_: dict):
        """
        Renames a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param input_: the GroupNameInput entity
        :return:
        """
        endpoint = '/groups/%s/name' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)

        # update group model's name
        self.name = result
        return result

    @check
    def set_description(self, input_: dict):
        """
        Sets the description of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param input_: the GroupDescriptionInput entity
        :return:
        """
        endpoint = '/groups/%s/description' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)

        # update group model's description
        self.description = result
        return result

    def delete_description(self):
        """
        Sets the description of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :return:
        """
        endpoint = '/groups/%s/description' % self.id
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

        # update group model's description
        self.description = None

    @check
    def set_options(self, input_: dict):
        """
        Sets the options of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param input_: the GroupOptionsInput entity
        :return:
        """
        endpoint = '/groups/%s/options' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)

        # update group model's options
        self.options = result
        return result

    @check
    def set_owner(self, input_: dict):
        """
        Sets the owner group of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param input_: the GroupOwnerInput entity
        :return:
        """
        endpoint = '/groups/%s/owner' % self.id
        base_url = self.gerrit.get_endpoint_url(endpoint)
        response = self.gerrit.requester.put(base_url, json=input_, headers=self.gerrit.default_headers)
        result = self.gerrit.decode_response(response)

        # update group model's owner and owner_id
        self.owner = result.get('owner')
        self.owner_id = result.get('owner_id')

        return self.gerrit.groups.get(result.get('owner_id'))

    def get_audit_log(self):
        """
        Gets the audit log of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :return:
        """
        endpoint = '/groups/%s/log.audit' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return result

    def index(self):
        """
        Adds or updates the internal group in the secondary index.

        :return:
        """
        endpoint = '/groups/%s/index' % self.id
        response = self.gerrit.requester.post(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def list_members(self):
        """
        Lists the direct members of a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :return:
        """
        endpoint = '/groups/%s/members/' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.accounts.get(member.get('username')) for member in result]

    def get_member(self, username: str):
        """
        Retrieves a group member.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param username: account username
        :return:
        """
        account = self.gerrit.accounts.get(username)
        endpoint = '/groups/%s/members/%s' % (self.id, str(account._account_id))
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get('username'))

    def add_member(self, account: GerritAccount):
        """
        Adds a user as member to a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param account: gerrit account
        :return:
        """
        endpoint = '/groups/%s/members/%s' % (self.id, str(account._account_id))
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.accounts.get(result.get('username'))

    def remove_member(self, account: GerritAccount):
        """
        Removes a user from a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param account: gerrit account
        :return:
        """
        endpoint = '/groups/%s/members/%s' % (self.id, str(account._account_id))
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()

    def list_subgroups(self):
        """
        Lists the direct subgroups of a group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :return:
        """
        endpoint = '/groups/%s/groups/' % self.id
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return [self.gerrit.groups.get(item.get('id')) for item in result]

    def get_subgroup(self, id_: str):
        """
        Retrieves a subgroup.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param id_: sub group id
        :return:
        """
        endpoint = '/groups/%s/groups/%s' % (self.id, id_)
        response = self.gerrit.requester.get(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.groups.get(result.get('id'))

    def add_subgroup(self, subgroup):
        """
        Adds an internal or external group as subgroup to a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param subgroup: gerrit subgroup
        :return:
        """
        endpoint = '/groups/%s/groups/%s' % (self.id, subgroup.id)
        response = self.gerrit.requester.put(self.gerrit.get_endpoint_url(endpoint))
        result = self.gerrit.decode_response(response)
        return self.gerrit.groups.get(result.get('id'))

    def remove_subgroup(self, subgroup):
        """
        Removes a subgroup from a Gerrit internal group.
        This endpoint is only allowed for Gerrit internal groups;
        attempting to call on a non-internal group will return 405 Method Not Allowed.

        :param subgroup: gerrit subgroup
        :return:
        """
        endpoint = '/groups/%s/groups/%s' % (self.id, subgroup.id)
        response = self.gerrit.requester.delete(self.gerrit.get_endpoint_url(endpoint))
        response.raise_for_status()
