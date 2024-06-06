from flask import Flask, render_template, request, redirect, url_for
import cv2

app = Flask(__name__)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def add_text_to_frame(frame, text, max_chars_per_line=0, position=(50, 50), font=cv2.FONT_HERSHEY_SIMPLEX,
                      font_scale=1, color=(0, 255, 0), thickness=2, line_spacing=30):
    # Split the text into lines with maximum characters per line
    lines = []
    current_line = ""
    for word in text.split():
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    if current_line:
        lines.append(current_line)

    # Add text lines to the frame
    y = position[1]
    for line in lines:
        cv2.putText(frame, line, (position[0], y), font, font_scale, color, thickness)
        y += line_spacing

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_to_add = request.form['text']
        max_chars_per_line = int(request.form['max_chars_per_line'])
        font_scale = float(request.form['font_scale'])
        thickness = int(request.form['thickness'])
        line_spacing = int(request.form['line_spacing'])
        width = int(request.form['width'])
        height = int(request.form['height'])

        # Always using image as background
        image_path = request.form['image_path']
        background = cv2.imread(image_path)
        if background is None:
            return render_template('index.html', error="Error: Unable to open the image.")
        background = cv2.resize(background, (width, height))

        # Add text to the frame
        add_text_to_frame(background, text_to_add, max_chars_per_line, font_scale=font_scale,
                          thickness=thickness, line_spacing=line_spacing)

        # Display the result
        cv2.imshow("Result", background)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return redirect(url_for('index'))  # Redirect to reload the page
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
