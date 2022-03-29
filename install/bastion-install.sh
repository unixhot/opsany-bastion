#!/bin/bash
#******************************************
# Author:       Jason Zhao
# Email:        zhaoshundong@opsany.com
# Organization: OpsAny https://www.opsany.com/
# Description:  OpsAny Bastion Install Script
#******************************************

# Get Data/Time
CTIME=$(date "+%Y-%m-%d-%H-%M")

# Shell Envionment Variables
CDIR=$(pwd)
SHELL_NAME="paas-install.sh"
SHELL_LOG="${CDIR}/${SHELL_NAME}.log"

# Shell Log Record
shell_log(){
    LOG_INFO=$1
    echo "----------------$CTIME ${SHELL_NAME} : ${LOG_INFO}----------------"
    echo "$CTIME ${SHELL_NAME} : ${LOG_INFO}" >> ${SHELL_LOG}
}

# Install Inspection
if [ ! -f ./install.config ];then
      echo "Please Copy install.config and Change: cp install.config.example install.config"
      exit
else
    source ./install.config
fi

# Check Install requirement
install_check(){
  DOCKER_PID=$(ps aux | grep '/usr/bin/containerd' | grep -v 'grep' | wc -l)
  if [ ${DOCKER_PID} -lt 1 ];then
      echo "Please install and start docker first!!!"
      exit
  fi
}

# Install Initialize
opsany_init(){
    shell_log "Start: Install Init"
    mkdir -p ${INSTALL_PATH}/{uploads/guacamole,logs,saas/apps,saas/saasapp}
    cd $CDIR
    /bin/cp -r ../install/conf ${INSTALL_PATH}/
    ## init for esb
    /bin/cp -r ../paas-ce/paas/esb/components/generic/apis/ ${INSTALL_PATH}/esb/
    shell_log "End: Install Init"
}

# PaaS Share Service Start
guacd_install(){
    # Guacd
    shell_log "======Start Guacd======"
    docker run -d --restart=always --name opsany-guacd \
    -p 4822:4822 \
    -v ${INSTALL_PATH}/uploads/guacamole:/srv/guacamole \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/guacd:1.2.0
}

# MySQL Initialize
mysql_init(){
    shell_log "======MySQL Initialize======"
    sleep 10
    cd ${CDIR}/../install/
    export MYSQL_PWD=${MYSQL_ROOT_PASSWORD}
    mysql -h "${MYSQL_SERVER_IP}" -u root -p"${MYSQL_ROOT_PASSWORD}" -e "create database bastion DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
    mysql -h "${MYSQL_SERVER_IP}" -u root -p"${MYSQL_ROOT_PASSWORD}" -e "grant all on bastion.* to paas@'%' identified by "\"${MYSQL_PAAS_PASSWORD}\"";"
    mysql -h "${MYSQL_SERVER_IP}" -u root -p"${MYSQL_ROOT_PASSWORD}" -e "grant all on bastion.* to bastion@'%' identified by "\"${MYSQL_OPSANY_BASTION_PASSWORD}\"";" 
}

# PaaS Configuration
paas_config(){
    shell_log "======PAAS Configuration======"
    # Websocket
    sed -i "s/WEBSOCKET_GUACD_HOST/${WEBSOCKET_GUACD_HOST}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
    sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
    sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
    sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
    sed -i "s/MYSQL_OPSANY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
    sed -i "s/demo.opsany.com/${PAAS_PAAS_IP}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket.init
    
    # OpenResty
    sed -i "s/DOMAIN_NAME/${DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/nginx-conf.d/nginx_paas.conf
    sed -i "s/LOCAL_IP/${LOCAL_IP}/g" ${INSTALL_PATH}/conf/nginx-conf.d/nginx_paas.conf
}

# PaaS Service Start
websocket_start(){
    #websocket
    shell_log "======Start websocket Service======"
    docker run -d --restart=always --name opsany-paas-websocket \
    -p 8004:8004 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket:/opt/opsany/websocket/config/prod.py \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket.init:/opt/opsany/websocket/config/__init__.py \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/opsany-paas-websocket:${PAAS_VERSION}
    
    #openresty
    shell_log "======Start openresty Service======"
    docker run -d --restart=always --name opsany-openresty \
    -p 80:80 -p 443:443 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/conf/nginx-conf.d:/etc/nginx/conf.d \
    -v ${INSTALL_PATH}/conf/nginx.conf:/etc/nginx/nginx.conf \
    -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/openresty:1.17.8.2-alpine

}

# Main
main(){
    install_check
    opsany_init
    guacd_install
    sleep 10
    mysql_init
    paas_config
    websocket_start
}

main
