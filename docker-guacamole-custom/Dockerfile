FROM guacamole/guacamole:1.5.5

COPY files/start.sh /opt/guacamole/bin/start.sh
COPY files/entrypoint.sh /opt/guacamole/bin/entrypoint.sh
COPY files/inject-trigger.sh /opt/guacamole/bin/inject-trigger.sh
COPY files/quickconnect /opt/guacamole/quickconnect

ARG RELEASE
ARG LAUNCHPAD_BUILD_ARCH
LABEL org.opencontainers.image.ref.name=ubuntu
LABEL org.opencontainers.image.version=22.04
CMD ["/bin/bash"]
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH=/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8
ENV JAVA_VERSION=jdk8u402-b06
ENTRYPOINT ["/__cacert_entrypoint.sh"]
ENV CATALINA_HOME=/usr/local/tomcat
ENV PATH=/usr/local/tomcat/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /usr/local/tomcat
ENV TOMCAT_NATIVE_LIBDIR=/usr/local/tomcat/native-jni-lib
ENV LD_LIBRARY_PATH=/usr/local/tomcat/native-jni-lib
ENV GPG_KEYS="05AB33110949707C93A279E3D3EFE6B686867BA6 07E48665A34DCAFAE522E5E6266191C37C037D42 47309207D818FFD8DCD3F83F1931D684307A10A5"
ENV TOMCAT_MAJOR=8
ENV TOMCAT_VERSION=8.5.98
ENV TOMCAT_SHA512=12f58114fe608fdc5f06e99a4ba01852396169f89d08e1ecf96ace36dd685c439519433e7750bfa7523f12c14788a3b5cb9ee3835dd1cce37e2cee121d69625e
EXPOSE 8080
ENTRYPOINT []
CMD ["catalina.sh" "run"]
WORKDIR /opt/guacamole
ARG UID=1001
ARG GID=1001
USER guacamole
EXPOSE 8080
CMD ["/opt/guacamole/bin/start.sh"]
