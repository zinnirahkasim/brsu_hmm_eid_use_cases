import rosbag

bag = rosbag.Bag('/home/zinnirah/ros/workspace/thesis/data/2013-03-11-16-12-59.bag')
for topic, msg, t in bag.read_messages(topics=['x_velocity_difference']):
    print msg
bag.close()