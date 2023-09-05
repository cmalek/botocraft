# This file is automatically generated by botocraft.  Do not edit directly.
# pylint: disable=anomalous-backslash-in-string,unsubscriptable-object,line-too-long,arguments-differ,arguments-renamed
# mypy: disable-error-code="index, override, assignment"
from collections import OrderedDict
from datetime import datetime
from typing import Any, ClassVar, Dict, List, Literal, Optional, cast

from pydantic import Field

from botocraft.services.common import Tag

from .abstract import (Boto3Model, Boto3ModelManager, PrimaryBoto3Model,
                       ReadonlyBoto3Model, ReadonlyBoto3ModelManager,
                       ReadonlyPrimaryBoto3Model)

# ===============
# Managers
# ===============


class RepositoryManager(Boto3ModelManager):
    service_name: str = "ecr"

    def create(
        self, model: "Repository", tags: Optional[List[Tag]] = None
    ) -> "Repository":
        """
        Create an ECR repository.

        Args:
            model: The :py:class:`Repository` to create.

        Keyword Args:
            tags: The metadata that you apply to the repository to help you categorize
                and organize them. Each tag consists of a key and an optional value, both
                of which you define. Tag keys can have a maximum character length of 128
                characters, and tag values can have a maximum length of 256 characters.
        """
        data = model.model_dump(exclude_none=True)
        args = dict(
            repositoryName=data["repositoryName"],
            registryId=data["registryId"],
            tags=self.serialize(tags),
            imageTagMutability=data["imageTagMutability"],
            imageScanningConfiguration=data["imageScanningConfiguration"],
            encryptionConfiguration=data["encryptionConfiguration"],
        )
        _response = self.client.create_repository(
            **{k: v for k, v in args.items() if v is not None}
        )
        response = CreateRepositoryResponse(**_response)
        return cast("Repository", response.repository)

    def delete(
        self,
        repositoryName: str,
        *,
        registryId: Optional[str] = None,
        force: bool = False
    ) -> "Repository":
        """
        Delete an ECR repository.

        Args:
            repositoryName: The name of the repository to delete.

        Keyword Args:
            registryId: The Amazon Web Services account ID associated with the registry
                that contains the repository to delete. If you do not specify a registry,
                the default registry is assumed.
            force:  If a repository contains images, forces the deletion.
        """
        args = dict(
            repositoryName=self.serialize(repositoryName),
            registryId=self.serialize(registryId),
            force=self.serialize(force),
        )
        _response = self.client.delete_repository(
            **{k: v for k, v in args.items() if v is not None}
        )
        response = DeleteRepositoryResponse(**_response)
        return cast(Repository, response.repository)

    def get(
        self, repositoryName: str, *, registryId: Optional[str] = None
    ) -> Optional["Repository"]:
        """
        Describes image repositories in a registry.

        Args:
            repositoryName: The name of the ECR repository to describe.

        Keyword Args:
            registryId: The Amazon Web Services account ID associated with the registry
                that contains the repositories to be described. If you do not specify a
                registry, the default registry is assumed.
        """
        args = dict(
            registryId=self.serialize(registryId),
            repositoryNames=self.serialize([repositoryName]),
        )
        _response = self.client.describe_repositories(
            **{k: v for k, v in args.items() if v is not None}
        )
        response = DescribeRepositoriesResponse(**_response)

        if response.repositories:
            return response.repositories[0]
        return None

    def list(
        self,
        *,
        registryId: Optional[str] = None,
        repositoryNames: Optional[List[str]] = None
    ) -> List["Repository"]:
        """
        Describes image repositories in a registry.

        Keyword Args:
            registryId: The Amazon Web Services account ID associated with the registry
                that contains the repositories to be described. If you do not specify a
                registry, the default registry is assumed.
            repositoryNames: A list of repositories to describe. If this parameter is
                omitted, then all repositories in a registry are described.
        """
        paginator = self.client.get_paginator("describe_repositories")
        args = dict(
            registryId=self.serialize(registryId),
            repositoryNames=self.serialize(repositoryNames),
        )
        response_iterator = paginator.paginate(
            **{k: v for k, v in args.items() if v is not None}
        )
        results: List["Repository"] = []
        for _response in response_iterator:
            response = DescribeRepositoriesResponse(**_response)
            if response.repositories:
                results.extend(response.repositories)
            else:
                break
        return results


# ==============
# Service Models
# ==============


class ImageScanningConfiguration(Boto3Model):
    """
    The image scanning configuration for a repository.
    """

    #: The setting that determines whether images are scanned after being pushed to a
    #: repository. If set to ``true``, images will be scanned after being pushed. If
    #: this parameter is not specified, it will default to ``false`` and images will
    #: not be scanned unless a scan is manually started with the [API\_StartImageScan]
    #: (https://docs.aws.amazon.com/AmazonECR/latest/APIReference/API_StartImageScan.h
    #: tml) API.
    scanOnPush: Optional[bool] = None


class EncryptionConfiguration(Boto3Model):
    """
    The encryption configuration for the repository.

    This determines how the contents of your repository are encrypted at rest.
    """

    #: The encryption type to use.
    encryptionType: Literal["AES256", "KMS"]
    #: If you use the ``KMS`` encryption type, specify the KMS key to use for
    #: encryption. The alias, key ID, or full ARN of the KMS key can be specified. The
    #: key must exist in the same Region as the repository. If no key is specified,
    #: the default Amazon Web Services managed KMS key for Amazon ECR will be used.
    kmsKey: Optional[str] = None


class Repository(PrimaryBoto3Model):
    """
    An object representing a repository.
    """

    objects: ClassVar[Boto3ModelManager] = RepositoryManager()

    #: The Amazon Resource Name (ARN) that identifies the repository. The ARN contains
    #: the ``arn:aws:ecr`` namespace, followed by the region of the repository, Amazon
    #: Web Services account ID of the repository owner, repository namespace, and
    #: repository name. For example,
    #: ``arn:aws:ecr:region:012345678910:repository/test``.
    repositoryArn: str = Field(frozen=True, default=None)
    #: The Amazon Web Services account ID associated with the registry that contains
    #: the repository.
    registryId: Optional[str] = None
    #: The name of the repository.
    repositoryName: str
    #: The URI for the repository. You can use this URI for container image ``push``
    #: and ``pull`` operations.
    repositoryUri: str = Field(frozen=True, default=None)
    #: The date and time, in JavaScript date format, when the repository was created.
    createdAt: datetime = Field(frozen=True, default=None)
    #: The tag mutability setting for the repository.
    imageTagMutability: Literal["MUTABLE", "IMMUTABLE"]
    #: The image scanning configuration for a repository.
    imageScanningConfiguration: ImageScanningConfiguration
    #: The encryption configuration for the repository. This determines how the
    #: contents of your repository are encrypted at rest.
    encryptionConfiguration: Optional[EncryptionConfiguration] = None

    @property
    def arn(self) -> Optional[str]:
        """
        Return the ARN of the model.   This is the value of the
        :py:attr:`repositoryArn` attribute.

        Returns:
            The ARN of the model instance.
        """
        return self.repositoryArn

    @property
    def name(self) -> Optional[str]:
        """
        Return the name of the model.   This is the value of the
        :py:attr:`repositoryName` attribute.

        Returns:
            The name of the model instance.
        """
        return self.repositoryName

    @property
    def pk(self) -> OrderedDict[str, Any]:
        return OrderedDict(
            {
                "repositoryName": self.repositoryName,
                "registryId": self.registryId,
            }
        )


# =======================
# Request/Response Models
# =======================


class CreateRepositoryResponse(Boto3Model):
    #: The repository that was created.
    repository: Optional[Repository] = None


class DeleteRepositoryResponse(Boto3Model):
    #: The repository that was deleted.
    repository: Optional[Repository] = None


class DescribeRepositoriesResponse(Boto3Model):
    #: A list of repository objects corresponding to valid repositories.
    repositories: Optional[List["Repository"]] = None
    #: The ``nextToken`` value to include in a future ``DescribeRepositories``
    #: request. When the results of a ``DescribeRepositories`` request exceed
    #: ``maxResults``, this value can be used to retrieve the next page of results.
    #: This value is ``null`` when there are no more results to return.
    nextToken: Optional[str] = None
