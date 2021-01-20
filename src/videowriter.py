#!/usr/bin/env python
# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함

import cv2
import numpy as np
import sys
import math
import rospy
import time
import os

from std_msgs.msg import Float64, UInt8, String
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import tf
#from SlidingWindow2 import Slidingwindow
from datetime import datetime



class line_traceee:
	def __init__(self):
		#print('init')
		self.sub_select_ang = rospy.Subscriber('/usb_cam/image_raw/compressed',CompressedImage, self.move_turtlebot,  queue_size = 1)
		self.now=datetime.now()
		self.out2 = cv2.VideoWriter('/home/turtlebot/Videos/10-10/original_{}-{}-{} {}-{}.avi'.format(self.now.year, self.now.month, self.now.day, self.now.hour,
                                                                      self.now.minute),cv2.VideoWriter_fourcc('M','J','P','G'), 10, (1280,720))
		
		self.bridge = CvBridge()
		  # for record		

	def __del__(self):
		self.out2.release()
	def move_turtlebot(self,img_data): ### left : -  ### right : +
		#rospy.on_shutdown(self.myhook)
		# print('move_turtlebot')
		try:
			cv_image = self.bridge.compressed_imgmsg_to_cv2(img_data, "bgr8")
		except CvBridgeError as e:
			#print(e)
			pass
		self.line_trace(cv_image)
		

	def line_trace(self, frame):
		##print('line_trace')
		print 'dididididi'
		frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)
		
		self.out2.write(frame)
		cv2.waitKey(1)
	
	def main(self):
		rospy.spin()

if __name__ == '__main__':
	rospy.init_node('line_trace')#, anonymous=True)
	node = line_traceee()
	node.main()



