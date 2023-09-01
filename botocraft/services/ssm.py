# This file is automatically generated by botocraft.  Do not edit directly.
# pylint: disable=anomalous-backslash-in-string,unsubscriptable-object,line-too-long,arguments-differ,arguments-renamed
# mypy: disable-error-code="index, override"
from datetime import datetime
from typing import ClassVar, Dict, List, Literal, Optional, cast

from pydantic import Field

from botocraft.services.tagging import Tag

from .abstract import (Boto3Model, Boto3ModelManager, PrimaryBoto3Model,
                       ReadonlyBoto3Model, ReadonlyBoto3ModelManager,
                       ReadonlyPrimaryBoto3Model)

# ===============
# Managers
# ===============


class ParameterManager(Boto3ModelManager):
    service_name: str = "ssm"

    def create(
        self,
        model: "Parameter",
        Description: Optional[str] = None,
        KeyId: Optional[str] = None,
        AllowedPattern: Optional[str] = None,
        Tags: Optional[List[Tag]] = None,
        Tier: Optional[Literal["Standard", "Advanced", "Intelligent-Tiering"]] = None,
        Policies: Optional[str] = None,
    ) -> int:
        """
        Add a parameter to the system.

        Args:
            model: The :py:class:`Parameter` to create.

        Keyword Args:
            Description: Information about the parameter that you want to add to the
                system. Optional but recommended.
            KeyId: The Key Management Service (KMS) ID that you want to use to encrypt
                a parameter. Use a custom key for better security. Required for parameters
                that use the ``SecureString`` data type.
            AllowedPattern: A regular expression used to validate the parameter value.
                For example, for String types with values restricted to numbers, you can
                specify the following: AllowedPattern=^\d+$
            Tags: Optional metadata that you assign to a resource. Tags enable you to
                categorize a resource in different ways, such as by purpose, owner, or
                environment. For example, you might want to tag a Systems Manager parameter
                to identify the type of resource to which it applies, the environment, or
                the type of configuration data referenced by the parameter. In this case,
                you could specify the following key-value pairs:
            Tier: The parameter tier to assign to a parameter.
            Policies: One or more policies to apply to a parameter. This operation
                takes a JSON array. Parameter Store, a capability of Amazon Web Services
                Systems Manager supports the following policy types:
        """
        data = model.model_dump()
        _response = self.client.put_parameter(
            Name=data["Name"],
            Value=data["Value"],
            Description=self.serialize(Description),
            Type=data["Type"],
            KeyId=self.serialize(KeyId),
            Overwrite=data["Overwrite"],
            AllowedPattern=self.serialize(AllowedPattern),
            Tags=self.serialize(Tags),
            Tier=self.serialize(Tier),
            Policies=self.serialize(Policies),
            DataType=data["DataType"],
        )
        response = PutParameterResult.model_construct(**_response)
        return cast(int, response.Version)

    def update(
        self,
        model: "Parameter",
        Description: Optional[str] = None,
        KeyId: Optional[str] = None,
        AllowedPattern: Optional[str] = None,
        Tags: Optional[List[Tag]] = None,
        Tier: Optional[Literal["Standard", "Advanced", "Intelligent-Tiering"]] = None,
        Policies: Optional[str] = None,
    ) -> int:
        """
        Add a parameter to the system.

        Args:
            model: The :py:class:`Parameter` to update.

        Keyword Args:
            Description: Information about the parameter that you want to add to the
                system. Optional but recommended.
            KeyId: The Key Management Service (KMS) ID that you want to use to encrypt
                a parameter. Use a custom key for better security. Required for parameters
                that use the ``SecureString`` data type.
            AllowedPattern: A regular expression used to validate the parameter value.
                For example, for String types with values restricted to numbers, you can
                specify the following: AllowedPattern=^\d+$
            Tags: Optional metadata that you assign to a resource. Tags enable you to
                categorize a resource in different ways, such as by purpose, owner, or
                environment. For example, you might want to tag a Systems Manager parameter
                to identify the type of resource to which it applies, the environment, or
                the type of configuration data referenced by the parameter. In this case,
                you could specify the following key-value pairs:
            Tier: The parameter tier to assign to a parameter.
            Policies: One or more policies to apply to a parameter. This operation
                takes a JSON array. Parameter Store, a capability of Amazon Web Services
                Systems Manager supports the following policy types:
        """
        data = model.model_dump()
        _response = self.client.put_parameter(
            Name=data["Name"],
            Value=data["Value"],
            Description=self.serialize(Description),
            Type=data["Type"],
            KeyId=self.serialize(KeyId),
            Overwrite=data["Overwrite"],
            AllowedPattern=self.serialize(AllowedPattern),
            Tags=self.serialize(Tags),
            Tier=self.serialize(Tier),
            Policies=self.serialize(Policies),
            DataType=data["DataType"],
        )
        response = PutParameterResult.model_construct(**_response)
        return cast(int, response.Version)

    def get(self, Name: str, *, WithDecryption: bool = True) -> Optional["Parameter"]:
        """
        Get information about one or more parameters by specifying multiple
        parameter names.

        Args:
            Name: The name of the parameter you want to query.

        Keyword Args:
            WithDecryption: Return decrypted secure string value. Return decrypted
                values for secure string parameters. This flag is ignored for ``String``
                and ``StringList`` parameter types.
        """
        _response = self.client.get_parameters(
            Names=self.serialize([Name]), WithDecryption=self.serialize(WithDecryption)
        )
        response = GetParametersResult.model_construct(**_response)

        if response.Parameters:
            return response.Parameters[0]
        return None

    def list(
        self,
        *,
        Filters: Optional[List["ParametersFilter"]] = None,
        ParameterFilters: Optional[List["ParameterStringFilter"]] = None
    ) -> List["ParameterMetadata"]:
        """
        Get information about a parameter.

        Keyword Args:
            Filters: This data type is deprecated. Instead, use ``ParameterFilters``.
            ParameterFilters: Filters to limit the request results.
        """
        paginator = self.client.get_paginator("describe_parameters")
        response_iterator = paginator.paginate(
            Filters=self.serialize(Filters),
            ParameterFilters=self.serialize(ParameterFilters),
        )
        results: List["ParameterMetadata"] = []
        for _response in response_iterator:
            response = DescribeParametersResult(**_response)
            if response.Parameters:
                results.extend(response.Parameters)
            else:
                break
        return results

    def delete(self, Name: str) -> None:
        """
        Delete a parameter from the system. After deleting a parameter, wait
        for at least 30 seconds to create a parameter with the same name.

        Args:
            Name: The name of the parameter to delete.
        """
        self.client.delete_parameter(Name=self.serialize(Name))


# ==============
# Service Models
# ==============


class Parameter(PrimaryBoto3Model):
    """
    An Amazon Web Services Systems Manager parameter in Parameter Store.
    """

    objects: ClassVar[Boto3ModelManager] = ParameterManager()

    #: The name of the parameter.
    Name: str
    #: The type of parameter. Valid values include the following: ``String``,
    #: ``StringList``, and ``SecureString``.
    Type: Literal["String", "StringList", "SecureString"]
    #: The parameter value.
    Value: Optional[str] = None
    #: The parameter version.
    Version: Optional[int] = Field(frozen=True, default=None)
    #: Either the version number or the label used to retrieve the parameter value.
    #: Specify selectors by using one of the following formats:
    Selector: Optional[str] = None
    #: Applies to parameters that reference information in other Amazon Web Services
    #: services. ``SourceResult`` is the raw result or response from the source.
    SourceResult: Optional[str] = None
    #: Date the parameter was last changed or updated and the parameter version was
    #: created.
    LastModifiedDate: Optional[datetime] = Field(frozen=True, default=None)
    #: The Amazon Resource Name (ARN) of the parameter.
    ARN: Optional[str] = Field(frozen=True, default=None)
    #: The data type of the parameter, such as ``text`` or ``aws:ec2:image``. The
    #: default is ``text``.
    DataType: Optional[str] = None

    @property
    def pk(self) -> Optional[str]:
        """
        Return the primary key of the model.   This is the value of the
        :py:attr:`Name` attribute.

        Returns:
            The primary key of the model instance.
        """
        return self.Name

    @property
    def arn(self) -> Optional[str]:
        """
        Return the ARN of the model.   This is the value of the :py:attr:`ARN`
        attribute.

        Returns:
            The ARN of the model instance.
        """
        return self.ARN

    @property
    def name(self) -> Optional[str]:
        """
        Return the name of the model.   This is the value of the
        :py:attr:`Name` attribute.

        Returns:
            The name of the model instance.
        """
        return self.Name


# =======================
# Request/Response Models
# =======================


class PutParameterResult(Boto3Model):
    #: The new version number of a parameter. If you edit a parameter value, Parameter
    #: Store automatically creates a new version and assigns this new version a unique
    #: ID. You can reference a parameter version ID in API operations or in Systems
    #: Manager documents (SSM documents). By default, if you don't specify a specific
    #: version, the system returns the latest parameter value when a parameter is
    #: called.
    Version: Optional[int] = None
    #: The tier assigned to the parameter.
    Tier: Optional[Literal["Standard", "Advanced", "Intelligent-Tiering"]] = None


class GetParametersResult(Boto3Model):
    #: A list of details for a parameter.
    Parameters: Optional[List["Parameter"]] = None
    #: A list of parameters that aren't formatted correctly or don't run during an
    #: execution.
    InvalidParameters: Optional[List[str]] = None


class ParametersFilter(Boto3Model):
    """
    This data type is deprecated.

    Instead, use ParameterStringFilter.
    """

    #: The name of the filter.
    Key: Literal["Name", "Type", "KeyId"]
    #: The filter values.
    Values: List[str]


class ParameterStringFilter(Boto3Model):
    """
    One or more filters.

    Use a filter to return a more specific list of results.
    """

    #: The name of the filter.
    Key: str
    #: For all filters used with DescribeParameters, valid options include ``Equals``
    #: and ``BeginsWith``. The ``Name`` filter additionally supports the ``Contains``
    #: option. (Exception: For filters using the key ``Path``, valid options include
    #: ``Recursive`` and ``OneLevel``.)
    Option: Optional[str] = None
    #: The value you want to search for.
    Values: Optional[List[str]] = None


class ParameterInlinePolicy(Boto3Model):
    """
    One or more policies assigned to a parameter.
    """

    #: The JSON text of the policy.
    PolicyText: Optional[str] = None
    #: The type of policy. Parameter Store, a capability of Amazon Web Services
    #: Systems Manager, supports the following policy types: Expiration,
    #: ExpirationNotification, and NoChangeNotification.
    PolicyType: Optional[str] = None
    #: The status of the policy. Policies report the following statuses: Pending (the
    #: policy hasn't been enforced or applied yet), Finished (the policy was applied),
    #: Failed (the policy wasn't applied), or InProgress (the policy is being applied
    #: now).
    PolicyStatus: Optional[str] = None


class ParameterMetadata(Boto3Model):
    """
    Metadata includes information like the ARN of the last user and the
    date/time the parameter was last used.
    """

    #: The parameter name.
    Name: Optional[str] = None
    #: The type of parameter. Valid parameter types include the following: ``String``,
    #: ``StringList``, and ``SecureString``.
    Type: Optional[Literal["String", "StringList", "SecureString"]] = None
    #: The ID of the query key used for this parameter.
    KeyId: Optional[str] = None
    #: Date the parameter was last changed or updated.
    LastModifiedDate: Optional[datetime] = None
    #: Amazon Resource Name (ARN) of the Amazon Web Services user who last changed the
    #: parameter.
    LastModifiedUser: Optional[str] = None
    #: Description of the parameter actions.
    Description: Optional[str] = None
    #: A parameter name can include only the following letters and symbols.
    AllowedPattern: Optional[str] = None
    #: The parameter version.
    Version: Optional[int] = None
    #: The parameter tier.
    Tier: Optional[Literal["Standard", "Advanced", "Intelligent-Tiering"]] = None
    #: A list of policies associated with a parameter.
    Policies: Optional[List["ParameterInlinePolicy"]] = None
    #: The data type of the parameter, such as ``text`` or ``aws:ec2:image``. The
    #: default is ``text``.
    DataType: Optional[str] = None


class DescribeParametersResult(Boto3Model):
    #: Parameters returned by the request.
    Parameters: Optional[List["ParameterMetadata"]] = None
    #: The token to use when requesting the next set of items.
    NextToken: Optional[str] = None


class DeleteParameterResult(Boto3Model):
    pass
