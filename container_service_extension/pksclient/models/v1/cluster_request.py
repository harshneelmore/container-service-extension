# coding: utf-8

"""
    PKS

    PKS API  # noqa: E501

    OpenAPI spec version: 1.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from container_service_extension.pksclient.models.v1.cluster_parameters import ClusterParameters  # noqa: F401,E501


class ClusterRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'plan_name': 'str',
        'network_profile_name': 'str',
        'parameters': 'ClusterParameters'
    }

    attribute_map = {
        'name': 'name',
        'plan_name': 'plan_name',
        'network_profile_name': 'network_profile_name',
        'parameters': 'parameters'
    }

    def __init__(self, name=None, plan_name=None, network_profile_name=None, parameters=None):  # noqa: E501
        """ClusterRequest - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._plan_name = None
        self._network_profile_name = None
        self._parameters = None
        self.discriminator = None

        self.name = name
        self.plan_name = plan_name
        if network_profile_name is not None:
            self.network_profile_name = network_profile_name
        self.parameters = parameters

    @property
    def name(self):
        """Gets the name of this ClusterRequest.  # noqa: E501


        :return: The name of this ClusterRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ClusterRequest.


        :param name: The name of this ClusterRequest.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def plan_name(self):
        """Gets the plan_name of this ClusterRequest.  # noqa: E501


        :return: The plan_name of this ClusterRequest.  # noqa: E501
        :rtype: str
        """
        return self._plan_name

    @plan_name.setter
    def plan_name(self, plan_name):
        """Sets the plan_name of this ClusterRequest.


        :param plan_name: The plan_name of this ClusterRequest.  # noqa: E501
        :type: str
        """
        if plan_name is None:
            raise ValueError("Invalid value for `plan_name`, must not be `None`")  # noqa: E501

        self._plan_name = plan_name

    @property
    def network_profile_name(self):
        """Gets the network_profile_name of this ClusterRequest.  # noqa: E501


        :return: The network_profile_name of this ClusterRequest.  # noqa: E501
        :rtype: str
        """
        return self._network_profile_name

    @network_profile_name.setter
    def network_profile_name(self, network_profile_name):
        """Sets the network_profile_name of this ClusterRequest.


        :param network_profile_name: The network_profile_name of this ClusterRequest.  # noqa: E501
        :type: str
        """

        self._network_profile_name = network_profile_name

    @property
    def parameters(self):
        """Gets the parameters of this ClusterRequest.  # noqa: E501


        :return: The parameters of this ClusterRequest.  # noqa: E501
        :rtype: ClusterParameters
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this ClusterRequest.


        :param parameters: The parameters of this ClusterRequest.  # noqa: E501
        :type: ClusterParameters
        """
        if parameters is None:
            raise ValueError("Invalid value for `parameters`, must not be `None`")  # noqa: E501

        self._parameters = parameters

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ClusterRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
