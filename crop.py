from PIL import Image
import numpy as np
import cv2
import os


def crop_to_aspect_ratio(input_file, output_file, height, width):
    # Open the input file
    with Image.open(input_file) as img:
        # Get the current width and height
        curr_width, curr_height = img.size

        # Calculate the target aspect ratio
        aspect_ratio = width / height

        # Determine which dimension to crop from
        if curr_width / curr_height > aspect_ratio:
            # Crop from the width
            crop_width = int(curr_height * aspect_ratio)
            crop_height = curr_height
            x_offset = (curr_width - crop_width) // 2
            y_offset = 0
        else:
            # Crop from the height
            crop_width = curr_width
            crop_height = int(curr_width / aspect_ratio)
            x_offset = 0
            y_offset = (curr_height - crop_height) // 2
        
        # Crop the image
        cropped_img = img.crop((x_offset, y_offset, x_offset + crop_width, y_offset + crop_height))
        
        # Save the cropped image to the output file
        output_file = os.path.join(output_file, os.path.basename(input_file))
        cropped_img.save(output_file.split(".")[0] + "-" + str(height) + "x" + str(width) + ".jpg")
        print("Finished crop: " + str(height) + "x" + str(width))


def create_video(input_file, output_file):
        # Load the image
        img = cv2.imread(input_file)

        # Downscale the image to 3840x2160 resolution
        img = cv2.resize(img, (3840, 2160))

        # Set the duration of the video in seconds
        duration = 5

        # Set the video dimensions
        height, width, channels = img.shape
        video_width = width
        video_height = height
        print(str(video_width))
        print(str(video_height))

        # Create a video writer object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(os.path.join(output_file, os.path.basename(input_file)) + "-video.mp4", fourcc, 25, (video_width, video_height))
        # video = cv2.VideoWriter("video.mp4", fourcc, 25, (video_width, video_height))

        # Iterate over each frame of the video
        for i in range(duration * 25):

            # Calculate the scaling factor for the current frame
            scale = 1 + i/float(duration * 25)/5

            # Create a scaling matrix for the current frame
            M = np.float32([[scale, 0, 0], [0, scale, 0]])

            # Apply the scaling matrix to the input image to create the current frame
            frame = cv2.warpAffine(img, M, (video_width, video_height))

            # Write the frame to the video
            video.write(frame)

        # Release the video writer object and close the video file
        video.release()
        cv2.destroyAllWindows()




def find_png_helper(list):
    for file in list:
        if ".png" in file:
            return file


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for file in os.listdir(script_dir + "/input/"):
        if file != ".DS_Store":
            print("Starting folder " + file)
            
            if "Crops" not in os.listdir(script_dir + "/input/" + file + "/"):
                os.mkdir(script_dir + "/input/" + file + "/Crops")
            if "Mockups" not in os.listdir(script_dir + "/input/" + file + "/"):
                os.mkdir(script_dir + "/input/" + file + "/Mockups")

            input_file_name = find_png_helper(os.listdir(script_dir + "/input/" + file + "/"))
            input_file_path = script_dir + "/input/" + file + "/" + input_file_name
            output_file_path = script_dir + "/input/" + file + "/Crops/" + input_file_name

            # create_video(input_file_path, output_file_path)
            
            ratios_h = [[5, 7], [8, 10], [11, 14], [16, 20], [20, 24], [20, 30], [22, 32], [24, 34], [30, 40]]
            ratios_v = [[5, 7], [8, 10], [11, 14], [12, 16], [12, 18], [16, 24], [18, 24], [20, 24], [20, 30], [24, 30], [24, 36]]

            if "v" in file:
                for i in range(len(ratios_v)):
                    crop_to_aspect_ratio(input_file_path, output_file_path, ratios_v[i][1], ratios_v[i][0])
            else:
                for i in range(len(ratios_h)):
                    crop_to_aspect_ratio(input_file_path, output_file_path, ratios_h[i][0], ratios_h[i][1])


if __name__ == '__main__':
    main()
