import streamlit as st
import os
import fitz  # PyMuPDF
from PIL import Image

# Function to list all PDF files in a directory
def list_pdfs(directory):
    return [f for f in os.listdir(directory) if f.endswith('.pdf')]

# Function to extract the first page of a PDF as an image
def get_first_page_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return image

# Main function to create the Streamlit app
def main():
    # Set the page configuration
    st.set_page_config(page_title="Learning Hub", page_icon=":books:", layout="wide")

    # Apply custom CSS for additional styling
    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f5f5;
            padding: 20px;
            font-family: Arial, sans-serif;
        }
        .title {
            font-size: 2.5em;
            color: #4b0082;
            text-align: center;
        }
        .subheader {
            font-size: 1.5em;
            color: #00008b;
            text-align: center;
        }
        .text {
            font-size: 1.2em;
            color: #333333;
            text-align: justify;
        }
        .sidebar-content {
            text-align: center;
        }
        .input-section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title
    st.markdown("<div class='title'>🎓 Hey there, Welcome to the Learning Hub! 🎓</div>", unsafe_allow_html=True)

    # Subheader
    st.markdown("<div class='subheader'>Enhance your knowledge with these materials 📚</div>", unsafe_allow_html=True)

    # Description
    st.markdown("<div class='text'>This website is designed to provide educational resources. You can download notes by entering your details below. Make the best use of these materials and work hard to achieve your goals. 🌟</div>", unsafe_allow_html=True)

    # Encouragement
    st.markdown("<div class='subheader'>Best of luck, my dear students! 🍀</div>", unsafe_allow_html=True)

    # Optional additional text or footer
    st.markdown("<div class='text'>Happy Learning! 😊</div>", unsafe_allow_html=True)
    
    # Sidebar with photo and qualifications
    st.sidebar.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.sidebar.image("mritunjay.png", use_column_width=True)
    st.sidebar.markdown(
        """
        ## Mritunjay Mishra
        
        Hello there! My name is Mritunjay Mishra. I have completed:
        - **B.Sc (PCM)** in 2017
        - **M.Sc (Physics)** in 2019
        - **B.Ed** in 2021

        With over 8 years of experience in the teaching department, my absolute goal is to help my students excel in their studies and motivate them to achieve their dreams. I work tirelessly to ensure my students achieve good marks. If you have been my student, you know the dedication and methods I bring to the classroom.

        Thank you for visiting my website. Feel free to drop any suggestions or recommendations!
        """
    )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    # Form for student details
    st.markdown("### Please fill in your details")
    with st.form(key='student_form'):
        class_selected = st.selectbox("Select your class", ["Class 9", "Class 10", "Class 11", "Class 12"])
        material_type = st.selectbox("Select material type", ["Notes", "Assignments", "Books"])
        submit_button = st.form_submit_button(label='Submit')

    # Display materials based on class selection
    if submit_button:
        st.write(f"Here are the {material_type.lower()} for {class_selected}:")
        
        # Directory based on class and material selection
        class_directories = {
            "Class 9": "class_9_materials",
            "Class 10": "class_10_materials",
            "Class 11": "class_11_materials",
            "Class 12": "class_12_materials"
        }
        material_directories = {
            "Notes": "notes",
            "Assignments": "assignments",
            "Books": "books"
        }
        directory = os.path.join(class_directories[class_selected], material_directories[material_type])
        
        if not os.path.exists(directory):
            st.write("Nothing is available here right now, come back later.")
        else:
            pdfs = list_pdfs(directory)
            if not pdfs:
                st.write("Nothing is available here right now, come back later.")
            else:
                # Display PDF previews and download links in a grid
                cols = st.columns(4)  # Create 4 columns
                for i, pdf in enumerate(pdfs):
                    pdf_path = os.path.join(directory, pdf)
                    image = get_first_page_image(pdf_path)
                    # Resize image to fit in a column
                    resized_image = image.resize((150, 200))
                    
                    with cols[i % 4]:  # Arrange images in grid
                        st.image(resized_image, caption=pdf, use_column_width=True)
                        with open(pdf_path, "rb") as file:
                            st.download_button(
                                label="Download",
                                data=file,
                                file_name=pdf,
                                mime='application/octet-stream'
                            )

if __name__ == '__main__':
    main()
