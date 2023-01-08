"""
AutoSender is a tool to send files as trxs to rum group, and download files from rum group.
"""

import datetime
import json
import logging
import os
import time

from mininode import MiniNode, create_private_key
from mininode.crypto import private_key_to_pubkey

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(f"auto_sender_{datetime.date.today()}.log", encoding="utf-8")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)


def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def read_json_file(filepath, default_data={}):
    data = default_data
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    return data


def write_json_file(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1, sort_keys=False, ensure_ascii=False)


def search_files_by_types(dir_path, filetypes=(".md", ".txt")):
    for root, paths, files in os.walk(dir_path):
        for f in files:
            if f.endswith(filetypes):
                yield os.path.join(root, f)


def init_rumdir(dirpath):
    rum_dir = os.path.join(dirpath, ".rum")
    if not os.path.exists(rum_dir):
        os.makedirs(rum_dir)
    return rum_dir


def is_content_same(content1, content2):
    a = content1.replace(" ", "").replace("\r", "").replace("\t", "")
    b = content2.replace(" ", "").replace("\r", "").replace("\t", "")
    return a == b


class AutoSender:
    def __init__(
        self,
        local_dir_path: str,
        rum_group_seed: str,
        private_key: str = None,
        filetypes=(".md", ".txt"),
        rum_version: int = 2,
        **kwargs,
    ):
        """
        Args:
            local_dir_path (str): the dir path of the files to be sent
            rum_group_seed (str): the seed of the rum group, which is used to send file as trx
            private_key (str): the private key of the rum group. If it is None, the private key will be generated automatically.
            filetypes (tuple, optional): the filetypes that will be sent to rum group. Defaults to (".md", ".txt").
            rum_version (int, optional): the version of rum, 1 or 2. Defaults to 2.
        """
        self.filetypes = filetypes
        self.local_dir_path = local_dir_path
        self.private_key = private_key
        self.seed = rum_group_seed
        if rum_version not in (1, 2):
            raise Exception("rum_version must be 1 or 2")
        self.rum = MiniNode(rum_group_seed, version=rum_version)
        self.info_file = self.init_infofile(self.local_dir_path)
        self.config_file = self.init_configfile(self.local_dir_path)

    def init_infofile(self, dirpath):
        """init filetrx_info.json file in the dirpath"""
        rum_dir = init_rumdir(dirpath)
        name = f"filetrx_info_{self.rum.api.group_id}.json"
        infofile = os.path.join(rum_dir, name)
        return infofile

    def init_configfile(self, dirpath):
        """init or check config.json"""
        rum_dir = init_rumdir(dirpath)
        name = f"config_{self.rum.api.group_id}.json"
        configfile = os.path.join(rum_dir, name)

        if not os.path.exists(configfile):
            if self.private_key is None:
                self.private_key = create_private_key()

            config = {
                "group_id": self.rum.api.group_id,
                "local_dir_path": dirpath,
                "rum_group_seed": self.seed,
                "private_key": [self.private_key],
                "filetypes": self.filetypes,
                "filetrx_infofile": self.info_file,
            }
            write_json_file(configfile, config)
        else:
            config = read_json_file(configfile)
            if config["group_id"] != self.rum.api.group_id:
                raise Exception("group_id not match")
            if config["local_dir_path"] != dirpath:
                raise Exception("local_dir_path not match")
            if config["rum_group_seed"] != self.seed:
                raise Exception("rum_group_seed not match")

            if self.private_key is None:
                self.private_key = config["private_key"][-1]
            elif self.private_key not in config["private_key"]:
                config["private_key"].append(self.private_key)
                write_json_file(configfile, config)

        return configfile

    def send_file_as_trx(self, filepath):
        """send file as trx to rum group"""
        info = read_json_file(self.info_file)
        flag = False
        content = read_file(filepath)
        relpath = os.path.relpath(filepath, self.local_dir_path)
        if relpath not in info:
            resp = self.rum.api.send_content(
                self.private_key,
                content=content,
                name=relpath,
                timestamp=os.path.getctime(filepath),
            )
            if "trx_id" in resp:
                info[relpath] = [resp["trx_id"]]
                flag = True
                logger.info("new trx %s", resp["trx_id"])
            else:
                logger.error("new trx error %s", resp)
        else:
            trx_id = info[relpath][-1]
            trx = self.rum.api.trx(trx_id)

            try:
                contentd = trx["Content"]["content"]
            except:
                logger.error("get trx %s error %s", trx_id, trx)
                return
            if not is_content_same(contentd, content):
                resp = self.rum.api.edit_trx(
                    self.private_key,
                    content=content,
                    name=relpath,
                    trx_id=trx_id,
                    timestamp=os.path.getmtime(filepath),
                )
                if "trx_id" in resp:
                    info[relpath].append(resp["trx_id"])
                    flag = True
                    logger.info("update trx %s", resp["trx_id"])
                else:
                    logger.error("update trx error %s", resp)

        if flag:
            write_json_file(self.info_file, info)
            logger.debug("auto_send is finished %s", relpath)

    def auto_sender(self):
        """auto send file as trx to rum group for all the files in the dirpath"""
        txtfiles = search_files_by_types(self.local_dir_path, self.filetypes)
        for ipath in txtfiles:
            self.send_file_as_trx(ipath)

    def download_by_info(self, todir, info_file):
        """download file from rum group by info_file"""
        info = read_json_file(info_file)
        for relpath, trx_ids in info.items():
            for trx_id in trx_ids:
                trx = self.rum.api.trx(trx_id)
                content = trx["Content"]["content"]
                name = trx["Content"]["name"]
                opath = os.path.join(todir, relpath)
                odir = os.path.dirname(opath)
                if not os.path.exists(odir):
                    os.makedirs(odir)
                if os.path.exists(opath):
                    contentd = read_file(opath)
                    if not is_content_same(contentd, content):
                        flag = True
                else:
                    flag = True
                if flag:
                    with open(opath, "w", encoding="utf-8") as f:
                        f.write(content)
                    logger.info("download %s to %s is finished", name, opath)

    def download_by_group(self, todir: str = None, senders: list = None):
        """download files from rum group without info_file"""
        if todir is None:
            todir = self.local_dir_path
        infofile = self.init_infofile(todir)
        config_file = self.init_configfile(todir)
        info = read_json_file(infofile)
        senders = senders or [private_key_to_pubkey(self.private_key)]
        trxs = self.rum.api.get_all_contents(senders=senders)
        for trx in trxs:
            trx_id = trx["TrxId"]
            try:
                content = trx["Content"]["content"]
                relpath = trx["Content"]["name"]
            except:
                continue
            opath = os.path.join(todir, relpath)
            odir = os.path.dirname(opath)
            if not os.path.exists(odir):
                os.makedirs(odir)
            if os.path.exists(opath):
                contentd = read_file(opath)
                if not is_content_same(contentd, content):
                    flag = True
            else:
                flag = True
            if flag:
                with open(opath, "w", encoding="utf-8") as f:
                    f.write(content)
                    logger.debug("download %s finished", relpath)

            if relpath not in info:
                info[relpath] = [trx_id]
                write_json_file(infofile, info)
            elif trx_id not in info[relpath]:
                info[relpath].append(trx_id)
                write_json_file(infofile, info)

    def update_profile(self, name, image):
        resp = self.rum.api.update_profile(self.private_key, name=name, image=image)
        logger.info("update profile %s", resp)
