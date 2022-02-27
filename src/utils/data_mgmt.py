import shutil
import imghdr
from PIL import Image
import os
from tqdm import tqdm
import logging
from src.utils.common import create_directories

def validate_image(config:dict)->None:
   PARENT_DIR = os.path.join(config["data"]["unzip_data_dir"], config["data"]["parent_data_dir"])
   BAD_DATA_DIR = os.path.join(config["data"]["unzip_data_dir"], config["data"]["bad_data_dir"])

   os.makedirs(BAD_DATA_DIR, exist_ok=True)
   for dirs in os.listdir(PARENT_DIR):
      full_path_data_dir = os.path.join(PARENT_DIR, dirs)
      for imgs in os.listdir(full_path_data_dir):
         path_to_img = os.path.join(full_path_data_dir, imgs)
         try:
               img = Image.open(path_to_img)
               img.verify()

               if len(img.getbands()) !=3 or imghdr.what(path_to_img) not in ['jpeg','png']:
                  bad_data_path = os.path.join(BAD_DATA_DIR, imgs)
                  shutil.move(path_to_img, bad_data_path)
                  continue

                  logging.info(f"{path_to_img} not of expected format")
         except Exception as e:
               logging.info(f"{path_to_img} not of expected format")
               bad_data_path = os.path.join(BAD_DATA_DIR, imgs)
               shutil.move(path_to_img, bad_data_path)
               logging.info(f"moved bad file from {path_to_img} to {bad_data_path}")
               logging.exception(e)
