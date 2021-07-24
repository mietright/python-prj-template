# coding: utf-8

import os
import hashlib
from pathlib import PurePath
from shutil import copyfile
import logging
from urllib.parse import urlparse

import requests
import boto3
from ibanchecker.exception import InvalidParams


logger = logging.getLogger(__name__)


def build_path(content: bytes, source_path: str, dest: str) -> str:
    hashsha = hashlib.sha256(content)
    path = PurePath(source_path)
    suffix = path.suffix
    return str(path.joinpath(dest, hashsha.hexdigest() + suffix))


async def download_from_s3(pdf_source_path, pdf_target):
    botos3 = boto3.client("s3")
    botos3.download_file(os.getenv("BUCKET_NAME"), pdf_source_path, pdf_target)


async def copy_local_file(source_path, destdir):
    with open(source_path, "rb") as fopen:
        content = fopen.read()
    dest_path = build_path(content, source_path, destdir)
    copyfile(source_path, dest_path)
    return dest_path


async def download_file(source, source_path, dest):
    """Download the file from http(s)"""
    resp = requests.get(source)
    resp.raise_for_status()
    dest_path = build_path(resp.content, source_path, dest)
    with open(dest_path, "wb") as fopen:
        fopen.write(resp.content)
    return dest_path


async def download(source, dest_dir):
    """
    Determine the protocol to fetch the pdf: http / s3 ...
    """

    parsedurl = urlparse(source)
    logger.info("dl %s, %s", parsedurl.scheme, parsedurl.path)
    if parsedurl.scheme == "file" or parsedurl.scheme == "":
        return await copy_local_file(parsedurl.path, dest_dir)
    if parsedurl.scheme == "s3":
        return await download_from_s3(source, dest_dir)
    if parsedurl.scheme == "http" or parsedurl.scheme == "https":
        return await download_file(source, parsedurl.path, dest_dir)

    raise InvalidParams(
        "Unsupported file source",
        {"scheme": parsedurl.scheme, "path": parsedurl.path},
    )
