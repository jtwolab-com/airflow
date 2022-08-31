kubectl apply -f storage_class_csi.yaml
kubectl patch storageclass csi-ssd -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
 --set nfs.server=192.168.0.39 \
 --set nfs.path=/nas
# kubectl patch storageclass nfs-client -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
# helm delete nfs-subdir-external-provisioner

# airflow helm chart install 후
# kubectl apply -f airflow-pod-launcher-role.yaml

# node
# sudo apt-get install nfs-common