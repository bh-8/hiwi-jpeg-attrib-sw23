FROM ubuntu AS default
    WORKDIR /home/attrib

    RUN apt-get update
    RUN apt-get upgrade -y

    RUN apt-get install python3 -y
    RUN apt-get install python3-pip -y
    RUN apt-get install libmagic1 -y

    RUN pip install --no-cache-dir --upgrade pip
    #RUN pip install --no-cache-dir progress
    RUN pip install --no-cache-dir python-magic

    #exiftool
    RUN apt-get install exiftool -y

    #binwalk
    RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
    RUN apt-get install binwalk -y

    #strings
    RUN apt-get install binutils -y

    #foremost
    RUN apt-get install foremost -y

    #imagemagick
    RUN apt-get install imagemagick -y

    #stegoveritas
    RUN pip install stegoveritas
    RUN stegoveritas_install_deps

    COPY ./attrib ./

    RUN apt-get clean

    ENTRYPOINT ["python3", "./main.py"]