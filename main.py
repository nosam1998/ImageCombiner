from PIL import Image
import os
import itertools
from typing import List
from shutil import rmtree


class ImageCombiner:
    def __init__(self, parent_start_folder="in", output_dir_name="out", output_file_ext=".png") -> None:
        self.output_file_ext = output_file_ext
        self.parent_start_folder = parent_start_folder
        self.output_dir_name = output_dir_name
        self.curr_dir = os.getcwd()
        self.working_dir = os.path.join(self.curr_dir, self.parent_start_folder)
        self.file_dict = dict()
        self.output_dir_abs_path = self.prep_output_dir()
        self.original_dir_order = self.get_folders_in_dir(self.working_dir)

        self.main()

    def custom_error_exit(self, msg: str, code: int) -> None:
        print(msg)
        exit(code)

    def helper_txt(self):
        help_file_name = os.path.join(self.output_dir_abs_path, "READ_ME_FIRST.txt")
        with open(help_file_name, "w") as f:
            f.write(f"The file name is structured like so... {'_'.join(k.name for k in self.original_dir_order)}.{self.output_file_ext}")

    def gen_output_filename(self, abs_paths: list) -> str:
        output_filename = []

        for path in abs_paths:
            head, tail = os.path.split(path)

            filename, temp_ext = tail.split(".")
            output_filename.append(filename)

        return f'{"_".join(output_filename)}{self.output_file_ext}'

    def prep_output_dir(self) -> str:
        output_dir_path = os.path.join(self.curr_dir, self.output_dir_name)
        if os.path.exists(output_dir_path):
            rmtree(output_dir_path)

        os.mkdir(output_dir_path)

        return output_dir_path

    def get_abs_filepath(self, path, folder, filename) -> str:
        return os.path.join(path, folder, filename)

    def prep_abs_paths(self) -> List[List[str]]:
        return [[self.get_abs_filepath(self.working_dir, k.name, f.name) for f in self.file_dict[k.name]] for k in self.original_dir_order]

    def get_all_combinations(self, abs_paths: List[List]) -> List[List]:
        return [list(combo) for combo in itertools.product(*abs_paths)]

    def check_size(self) -> bool:
        set_of_sizes = set()
        # Verify that all of the files are the same dimensions.
        for folder_name in self.file_dict:
            for file in self.file_dict[folder_name]:
                temp_filename = self.get_abs_filepath(self.working_dir, folder_name, file)
                with Image.open(temp_filename) as img:
                    if (img.width, img.height) not in set_of_sizes and len(set_of_sizes) > 0:
                        print(f"Incorrect dimensions for: {temp_filename}")
                        return False
                    elif (img.width, img.height) not in set_of_sizes:
                        set_of_sizes.add((img.width, img.height))

        return True

    def get_files_in_dir(self, path) -> list:
        with os.scandir(path) as i:
            return [d for d in i if d.is_file()]

    def get_folders_in_dir(self, path) -> list:
        with os.scandir(path) as i:
            return [d for d in i if d.is_dir()]

    def combine_images(self, img_abs_paths: list):
        if len(img_abs_paths) < 2:
            self.custom_error_exit("Only got 1 image! You need at least 2 images to combine! Exiting...", 0)
        orig = Image.open(img_abs_paths[0])
        for img_path in img_abs_paths[1:]:
            with Image.open(img_path) as temp_img:
                # orig.paste(temp_img)
                orig.alpha_composite(temp_img)

        abs_file_path = os.path.join(self.output_dir_abs_path, self.gen_output_filename(img_abs_paths))
        orig.save(abs_file_path)

    def combine_images_driver(self, all_combos: List[List]) -> None:
        for combo in all_combos:
            self.combine_images(combo)

    def custom_layer_order_help_message(self, available):
        print("Please select each layer in the order you'd like them...")
        print("Type the number next to the name to select.")
        for i, a in available:
            print(f"{i}: {a.name}")
        user_input = input("Pick a number >>> ")
        return int(user_input) if user_input.isnumeric() else self.custom_layer_order_help_message(available)

    def custom_layer_order(self, numbered_order) -> list:
        new_dir_order = []

        while len(new_dir_order) < len(self.original_dir_order):
            answer = self.custom_layer_order_help_message(numbered_order)

            for idx, el in enumerate(numbered_order):
                if el[0] == answer:
                    new_dir_order.append(el[1])
                    del numbered_order[idx]

        return new_dir_order

    def main(self) -> None:
        custom_layer_order_answer = input("Would you like to use a custom order of the layers? Type Y or N\n> ")
        if "y" in custom_layer_order_answer.lower():
            self.original_dir_order = self.custom_layer_order(list(enumerate(self.original_dir_order)))

        for folder in self.original_dir_order:
            self.file_dict[folder.name] = self.get_files_in_dir(f"{self.working_dir}/{folder.name}")

        # Check if all of the images are the same size
        if not self.check_size():
            exit(0)

        abs_paths = self.prep_abs_paths()
        abs_path_combos = self.get_all_combinations(abs_paths)

        self.combine_images_driver(abs_path_combos)
        self.helper_txt()


ic = ImageCombiner()