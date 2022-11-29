import boto3
import json
def lambda_handler(event, context):

    cloud_break_count = 0 
    tagged_now =   0
    cant_tag   =   0
    alrdy_tagged = 0
    all_ecs_count = 0


    regions = ["eu-west-1","eu-west-2","us-east-1"]

    for region in regions:
        client = boto3.client("ecs", region_name=region)
        clusters = client.list_clusters()
        cluster_names = clusters['clusterArns']

        for cluster_name in cluster_names:
            paginator = client.get_paginator('list_services')

            response_iterator = paginator.paginate(
                cluster=cluster_name,
                PaginationConfig={
                'PageSize':100})

            for each_page in response_iterator:
                for each_arn in each_page['serviceArns']:
                    cloud_break_count += 1

                    if ( cloud_break_count == 5 ):
                        time.sleep(1)
                        cloud_break_count = 0

                    all_ecs_count += 1
                    print(each_arn)
                    response_tags = client.list_tags_for_resource(resourceArn=each_arn)

                    flag = 0 

                    try:
                        all_tags = response_tags['response_tags']
                        for tag in all_tags:
                            if ( tag['Key'] == 'map-migrated' ):
                                flag =1
                                alrdy_tagged += 1

                    except Exception as e:
                        print(e)

                    if ( flag == 0 ):
                        try:
                            response = client.tag_resource(resourceArn=each_arn,tags=[{
                            'key': 'map-migrated',
                            'value': 'd-server-00a0posufm7nfr'}])
                            tagged_now += 1

                        except Exception as e:
                            print(e)
                            cant_tag += 1


                    
  print('all ecs  count',all_ecs_count)
  print('already tagged count' ,alrdy_tagged )
  print('tagged from this attempt',tagged_now)
  print('refused to tag',cant_tag )






