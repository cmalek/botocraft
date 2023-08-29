from typing import Optional, Any
from pydantic import BaseModel, ConfigDict

import boto3


class Boto3Model(BaseModel):
    """
    The base class for all boto3 models.
    """
    model_config = ConfigDict(validate_assignment=True)


class ReadonlyBoto3Model(Boto3Model):
    """
    The base class for all boto3 models that are readonly.
    """
    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True
    )


class Boto3ModelManager:

    #: The name of the boto3 service.  Example: ``ec2``, ``s3``, etc.
    service_name: str

    def __init__(self) -> None:
        #: The boto3 client for the AWS service
        self.client = boto3.client(self.service_name)  # type: ignore

    def serialize(
        self, arg: Any,
        exclude_none: bool = False,
    ) -> Any:
        """
        Some of our methods use :py:class:`Boto3Model` objects as arguments, but
        boto3 expects simple Python types.  This method will serialize the model
        into a set of types that boto3 will understand if it is a
        :py:class:`Boto3Model` object.

        If ``arg`` is not a :py:class:`Boto3Model` object, it will be returned
        verbatim.

        Args:
            arg: the botocraft method argument to serialize.

        Keyword Args:
            exclude_none: If ``True``, exclude any arguments that are ``None``.
                from the serialized output.

        Returns:
            A properly serialized argument.
        """
        if isinstance(arg, Boto3Model):
            return arg.model_dump(exclude_none=exclude_none)
        return arg

    def create(self, model, **kwargs):
        raise NotImplementedError

    def update(self, model, **kwargs):
        # Some models cannot be updated, so instead of raising a
        # NotImplementedError, we raise a RuntimeError.
        raise RuntimeError("This model cannot be updated.")

    def delete(self, pk: str, **kwargs):
        raise NotImplementedError


class ReadonlyBoto3ModelManager(Boto3ModelManager):

    def create(self, model, **kwargs):
        raise RuntimeError("This model cannot be created.")

    def delete(self, pk: str, **kwargs):
        raise RuntimeError("This model cannot be deleted.")


class ModelIdentityMixin:

    @property
    def pk(self) -> Optional[str]:
        """
        Get the primary key of the model instance.

        Returns:
            The primary key of the model instance.
        """
        raise NotImplementedError

    @property
    def arn(self) -> Optional[str]:
        """
        Get the ARN of the model instance.

        Returns:
            The ARN of the model instance.
        """
        raise ValueError("The model does not have an ARN.")

    @property
    def name(self) -> Optional[str]:
        """
        Get the name of the model instance.

        Returns:
            The name of the model instance.
        """
        raise ValueError("The model does not have a name.")


class ReadonlyPrimaryBoto3Model(  # pylint: disable=abstract-method
    ModelIdentityMixin,
    ReadonlyBoto3Model
):

    #: The manager for this model
    manager: Boto3ModelManager

    def save(self, **kwargs):
        """
        Save the model.
        """
        raise RuntimeError("Cannot save a readonly model.")

    def delete(self):
        """
        Delete the model.
        """
        raise RuntimeError("Cannot delete a readonly model.")


class PrimaryBoto3Model(  # pylint: disable=abstract-method
    ModelIdentityMixin,
    Boto3Model
):
    """
    The base class for all boto3 models that get returned as the primary object
    from a boto3 operation.
    """

    #: The manager for this model
    manager: Boto3ModelManager

    def save(self, **kwargs):
        """
        Save the model.
        """
        if self.pk:
            return self.manager.update(self, **kwargs)
        return self.manager.create(self, **kwargs)

    def delete(self):
        """
        Delete the model.
        """
        if not self.pk:
            raise ValueError("Cannot delete a model that has not been saved.")
        return self.manager.delete(self.pk)