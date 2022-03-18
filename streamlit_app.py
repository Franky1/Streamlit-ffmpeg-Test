import pathlib
import subprocess

import ffmpeg
import streamlit as st

# global variables
uploaded_mp3_file = None
uploaded_mp3_file_length = 0
filename = None
downloadfile = None


@st.experimental_memo
def convert_mp3_to_wav_ffmpeg_bytes2bytes(input_data: bytes) -> bytes:
    """
    It converts mp3 to wav using ffmpeg.

    :param input_data: bytes object of a mp3 file
    :return: a bytes object of a wav file
    """
    args = (ffmpeg
            .input('pipe:', format='mp3')
            .output('pipe:', format='wav')
            .global_args('-loglevel', 'error')
            .get_args()
            )
    # print(args)
    proc = subprocess.Popen(
        ['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc.communicate(input=input_data)[0]


@st.experimental_memo
def on_file_change(uploaded_mp3_file):
    return convert_mp3_to_wav_ffmpeg_bytes2bytes(uploaded_mp3_file.getvalue())


# The below code is a simple streamlit web app that allows you to upload an mp3 file
# and then download the converted wav file.
if __name__ == '__main__':
    st.title('MP3 to WAV Converter test app')
    st.markdown('This app converts mp3 to wav using ffmpeg')
    uploaded_mp3_file = st.file_uploader('Upload Your MP3 File', type=['mp3'])

    if uploaded_mp3_file is not None:
        uploaded_mp3_file_length = len(uploaded_mp3_file.getvalue())
        filename = pathlib.Path(uploaded_mp3_file.name).stem
        if uploaded_mp3_file_length > 0:
            st.text(f'Size of uploaded "{uploaded_mp3_file.name}" file: {uploaded_mp3_file_length} bytes')
            downloadfile = on_file_change(uploaded_mp3_file)

    st.markdown("""---""")
    if downloadfile:
        length = len(downloadfile)
        if length > 0:
            st.subheader('After conversion to WAV you can download it below')
            st.download_button(label="Download .wav file",
                            data=downloadfile,
                            file_name=f'{filename}.wav',
                            mime='audio/wav')
            st.text(f'Size of "{filename}.wav" file to download: {length} bytes')
