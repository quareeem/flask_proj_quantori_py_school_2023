# Flask Blog Application

This is a Flask-based blog application where users can register, create, and manage posts.

## Getting Started

These instructions will cover usage information and for the docker container 

### Prerequisites

In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

### Installation and Usage

To get the application running, follow these steps:

After cloning repository run the following command:

```shell
docker-compose up --build
```

If container launched successfully, then you can proceed to the main page and start using the app. Please register and login there:

```shell
http://127.0.0.1:8000
```

This endpoint should look like this:

<img width="1440" alt="Снимок экрана 2023-11-06 в 17 53 12" src="https://github.com/quareeem/flask_proj_quantori_py_school_2023/assets/120713656/80926009-f9fc-4b26-9870-37c6b836ca93">








Admin panel is here. You may need to create new Groups here:
```shell
http://127.0.0.1:8000/admin
```

Admin panel should look like this:

<img width="1440" alt="Снимок экрана 2023-11-06 в 17 53 29" src="https://github.com/quareeem/flask_proj_quantori_py_school_2023/assets/120713656/6246da06-b039-4898-9fd6-56a5794b37c0">










Make sure that you login on the main page not in the admin panel.

After that you are free to create new Posts, and explore the app.
