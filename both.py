import cv2

def show_media(media_path, is_video=False, text="", text_size=1, text_color=(255, 255, 255)):
    if is_video:
        play_video(media_path, text, text_size, text_color)
    else:
        show_image(media_path, text, text_size, text_color)

def show_image(image_path, text="", text_size=1, text_color=(255, 255, 255)):
    # Read the image
    image = cv2.imread(image_path)

    # Check if image is read successfully
    if image is None:
        print("Error: Unable to read image.")
        return

    # Add text overlay if provided
    if text:
        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, text_size, text_color, 2)

    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def play_video(video_path, text="", text_size=1, text_color=(255, 255, 255)):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video.isOpened():
        print("Error: Unable to open video.")
        return

    # Read the first frame to get video dimensions
    ret, frame = video.read()
    if not ret:
        print("Error: Unable to read the video frame.")
        return

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_video = cv2.VideoWriter('output_video.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))

    # Read and display video frames until the video ends
    while video.isOpened():
        ret, frame = video.read()  # Read a frame
        if ret:
            if text:
                # Add text overlay to the frame
                cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, text_size, text_color, 2)
            cv2.imshow('Video', frame)  # Display the frame
            output_video.write(frame)  # Write the frame to the output video file
            if cv2.waitKey(25) & 0xFF == ord('q'):  # Press 'q' to quit
                break
        else:
            break

    # Release resources
    video.release()
    output_video.release()
    cv2.destroyAllWindows()

# Ask user whether to display an image or a video
media_type = input("Enter 'image' to display an image or 'video' to play a video: ").lower()

# Prompt user to enter the path of the media file
media_path = input("Enter the path of the media file: ")

# Prompt user to enter text overlay
text = input("Enter the text to overlay (press enter to skip): ")

# Prompt user to enter text size
text_size = float(input("Enter the text size (default is 1): "))

# Prompt user to enter text color (in BGR format)
text_color = input("Enter the text color as a comma-separated BGR value (e.g., 255,255,255 for white): ")
text_color = tuple(map(int, text_color.split(',')))

# Call the function to show the media with specified options
show_media(media_path, media_type == 'video', text, text_size, text_color)
