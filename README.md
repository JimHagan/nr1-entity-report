# nr1-entity-report
Simple tool for extracting a report of all New Relic monitored entities available to a user based on his user key.  Currently supports INFRA HOST, APM APPLICTION, and BROWSER APPLICATION

## Getting started

1. Clone the repository
2. CD into the repository directory
3. Create a Python 3 virtual environment, install dependencies, and activate it.

```
virtualenv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
```

4. Set the USER_API_KEY environment variable 

```
export USER_API_KEY=A_NEW_RELIC_USER_API_KEY
```

5. Run the program

There are currently three entity domains supported

- INFRA
- APM
- BROWSER
- MOBILE
- SYNTH

Let's run it with the INFRA domain.

```
python nr1-entity-report.py INFRA
```

You should see a nice summary of host counts broken down by account like so:

```
###### Report Summary ##########
Entity Domain: INFRA
Number of Accounts: 6
Total Number of Entities: 260
###### Account Breakdown #######
Video Demo: 4
Demotron V2: 78
GCP DEMO: 21
Demotron Rotate: 73
Demotron Distributed Tracing: 17
Demotron_CAS: 67
```

6. Explore and analyze the output file `nr1-entity-report.csv`

NOTE: This file will vary greatly as it pulls together all tags associated with the entities in a given set of accounts.  

here is a sample field list from an INFRA summary (pulled using the NR1 user `demonewrelic@gmail.com`)...

```
apmApplicationNames,label.Team,host,label.DEVELOPMENT_TEAM_NAME,label.k8s.io/cluster-autoscaler/node-template/label/kops.k8s.io/instancegroup,label.tier,gcp.networkTag.gke-hatshop-21f65cf4-node,label.deployedBy,aws.ec2AmiId,trustedAccountId,label.owningTeam,hostname,aws.ec2State,providerAccountId,team,aws.arn,label.KubernetesCluster,label.k8s.io/cluster-autoscaler/tinyhats-1004-1,label.dxDepartment,label.dxDeploymentName,organization,label.department,label.kubernetes.io/cluster/towersrotate.k8s.local,linuxDistribution,label.eks:cluster-name,label.goog-gke-node,aws.awsAvailabilityZone,aws.ec2Architecture,aws.ec2EbsOptimized,dxEnvironment,aws.awsRegion,label.dxDeployerVersion,hostStatus,label.product,class,agentName,gcp.zone,apmApplicationIds,label.aws:ec2launchtemplate:id,gcp.apmApplicationIds,gcp.clusterName,label.dxDeploymentDate,label.Tier,gcp.networkTag.gke-ageri-7401861c-node,aws.ec2InstanceType,aws.ec2PrivateDnsName,clusterName,gcp.projectId,gcp.name,dxDeployerVersion,operatingSystem,dxDeployedBy,label.kubernetes.io/cluster/towerssprod.k8s.local,label.CX,environment,dxProduct,aws.ec2InstanceId,aws.ec2PlacementGroupTenancy,gcp.networkTag.gke-local-58a3db9d-node,label.dxProduct,label.kops.k8s.io/instancegroup,ec2InstanceType,guid,alertsTest,owning_team,aws.ec2VirtualizationType,label.k8s.io/cluster-autoscaler/tinyhats-09102021,fullHostname,gcp.apmApplicationNames,label.k8s.io/cluster-autoscaler/node-template/label/group,label.alpha.eksctl.io/nodegroup-type,label.owning_team,dxOwningTeam,label.dxOwningTeam,dxDeploymentName,type,aws.accountId,agentVersion,label.kubernetes.io/cluster/umbraprod.k8s.local,label.environment,label.k8s.io/role/master,gcp.isPreemptible,label.k8s.io/cluster-autoscaler/node-template/label/environment,label.Business,label.Name,aws.ec2PrivateIpAddress,aws.ec2SubnetId,product,label.Chain,aws.ec2PublicDnsName,label.kubernetes.io/cluster/tinyhats-09102021,aws.ec2KeyName,awsRegion,label.dxDeployedBy,label.alpha.eksctl.io/nodegroup-name,label.aws:ec2launchtemplate:version,kernelVersion,dxDepartment,gcp.networkTag.gke-paulo-4fb368c2-node,gcp.machineType,coreCount,account,label.kubernetes.io/cluster/tinyhats-1004-1,dxDeploymentDate,label.eks:nodegroup-name,label.dxEnvironment,label.k8s.io/role/node,label.deploymentName,aws.ec2VpcId,label.aws:ec2:fleet-id,instanceType,label.k8s.io/cluster-autoscaler/node-template/label/owning_team,aws.ec2Hypervisor,label.k8s.io/cluster-autoscaler/enabled,label.group,label.DB,label.Service,aws.ec2PublicIpAddress,service,gcp.status,label.k8s.io/cluster-autoscaler/node-template/label/product,label.Services,processorCount,providerAccountName,aws.ec2RootDeviceType,label.aws:autoscaling:groupName,aws.ec2RootDeviceName,label.kubernetes.io/cluster/umbrarotate.k8s.local,accountId,displayName,systemMemoryBytes
```

here is sample row from that same INFRA summary...

```
Order-Assembly			UMBRA	nodes			demotronnr@newrelic.com	ami-0008325f0ded04d04	2119955		ip-172-20-45-212	running	14140		arn:aws:ec2:us-west-2:412066592467:instance/i-0446fdc886e2540a3	umbrarotate.k8s.local							Debian GNU/Linux 9 (stretch)			us-west-2a	x86_64	FALSE		us-west-2		running	demotron		Infrastructure		657681470							t3a.small	ip-172-20-45-212.us-west-2.compute.internal	umbrarotate.k8s.local				linux						i-0446fdc886e2540a3	default			nodes		MjExOTk1NXxJTkZSQXxOQXwzMzE4MjU5NzIxNTA1NDkwNjMz			hvm		ip-172-20-45-212.us-west-2.compute.internal		SITE		DEMO					412066592467	1.14.2		us-production			us-production		nodes.umbrarotate.k8s.local	172.20.45.212	subnet-04f08cac391cfe455			ec2-54-188-157-201.us-west-2.compute.amazonaws.com		kubernetes.umbrarotate.k8s.local-23:16:7a:dc:e3:e9:e0:54:2c:2e:5c:e1:71:f5:da:e3					4.9.0-7-amd64				1	Demotron Rotate					1		vpc-0f32eb8961ab0b2e0		t3a.small	DEMO	xen		SITE			54.188.157.201			demotron		2	Rotate AWS Integration	ebs	nodes.umbrarotate.k8s.local	/dev/xvda	owned	2119955	ip-172-20-45-212.us-west-2.compute.internal	2068160512
```