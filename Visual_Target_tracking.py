import numpy as np
import cv2

global x_step
global y_step
global R


def image_name(n):	
	base_name = 'image_girl'	
	if n<10:
		pre = "000"
	elif n<100:
		pre = "00"
	else:
		pre = "0"
	name = base_name + '/'+ str(pre)+ str(n)+'.jpg'
	return name

def SSD(T_x,T_y,gold_img,img,gray_img):
	current_img = img 
	gc_img = gray_img
	D = 0
	MIN_D = 10000000000000
	I_x = 0
	I_y = 0
	for i in range(T_x - x_step, T_x + x_step+1): #I_x
		for j in range(T_y - y_step, T_y + y_step+1): #I_y
			# print(i)
			# print(j)
			for c_x in range(i-R,i+R+1):
				for c_y in range(j-R,j+R+1):
					# print(c_x)
					# print(c_y)
					if (c_x - i)**2  + (c_y - j)**2 < R **2: #poinit (c_x,c_y) is in the circle
						old_x = T_x + i - c_x 
						old_y = T_y + j - c_y
						D += (int(gc_img[c_x,c_y]) - int(gold_img[old_x,old_y]))**2
						# print(D)
			# print(MIN_D)
			if D < MIN_D:
				MIN_D = D
				D = 0
				I_x = i 
				I_y = j
				# print('T_x is:')
				# print(T_x)
				# print('T_y is:')
				# print(T_y)
			else:
				pass
			D = 0
	
	T_x = I_x 
	T_y = I_y		
	gold_img = gc_img
	# print('T_x is:')
	# print(T_x)
	# print('T_y is:')
	# print(T_y)
	cv2.circle(current_img, (T_y, T_x), R, (0, 0, 255), 2)
	video.write(current_img)

def CC(T_x,T_y,gold_img,img,gray_img):
	current_img = img 
	gc_img = gray_img
	C = 0
	MAX_C = 0
	I_x = 0
	I_y = 0
	for i in range(T_x - x_step, T_x + x_step+1): #I_x
		for j in range(T_y - y_step, T_y + y_step+1): #I_y
			for c_x in range(i-R,i+R+1):
				for c_y in range(j-R,j+R+1):
					if (c_x - i)**2  + (c_y - j)**2 < R **2: #poinit (c_x,c_y) is in the circle
						old_x = T_x + i - c_x 
						old_y = T_y + j - c_y
						C += int(gc_img[c_x,c_y]) * int(gold_img[old_x,old_y])
			if C > MAX_C:
				MAX_C = C
				C = 0
				I_x = i 
				I_y = j
			else:
				pass
			C = 0	
	T_x = I_x 
	T_y = I_y		
	gold_img = gc_img

	cv2.circle(current_img, (T_y, T_x), R, (0, 0, 255), 2)
	video.write(current_img)

def NCC(T_x,T_y,gold_img,img,gray_img):
	current_img = img 
	gc_img = gray_img
	rows,columns = gray_img.shape
	NOP = rows * columns
	T = 0
	I = 0
	for r in range(rows):
		for c in range(columns):
			T += gold_img[r,c]
			I += gc_img[r,c] 
	Ta = T / NOP 
	Ia = I / NOP 
	N = 0
	T_sum = 0
	I_sum = 0
	M_sum = 0
	MAX_N = 0
	I_x = 0
	I_y = 0
	for i in range(T_x - x_step, T_x + x_step+1): #I_x
		for j in range(T_y - y_step, T_y + y_step+1): #I_y
			for c_x in range(i-R,i+R+1):
				for c_y in range(j-R,j+R+1):
					if (c_x - i)**2  + (c_y - j)**2 < R **2: #poinit (c_x,c_y) is in the circle
						old_x = T_x + i - c_x 
						old_y = T_y + j - c_y
						Ts = gold_img[old_x,old_y] - Ta 
						# print('Ts is: %s',Ts)
						Is = gc_img[c_x,c_y] - Ia 
						# print('Is is: %s',Is)
						T_sum += Ts ** 2
						I_sum += Is ** 2 
						M_sum += Ts * Is 

			# print('Tsum is: %s',T_sum)	
			# print('Isum is: %s',I_sum)		
			N = M_sum/np.sqrt(T_sum*I_sum)
			# print(M_sum/np.sqrt(T_sum*I_sum))

			if N > MAX_N:
				MAX_N = N
				T_sum = I_sum = M_sum = 0
				I_x = i 
				I_y = j
			else:
				pass
			N = 0
	
	T_x = I_x 
	T_y = I_y		
	gold_img = gc_img
	cv2.circle(current_img, (T_y, T_x), R, (0, 0, 255), 2)
	video.write(current_img)

			
N = 500
T_x = 44
T_y = 72
R = 25
x_step = 5
y_step = 8
video = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*"XVID"),30,(128,96))
name = image_name(1)
old_img = cv2.imread(name)  #initialize old_img
gold_img = cv2.cvtColor(old_img, cv2.COLOR_BGR2GRAY)  #initialize gold_img
cv2.circle(old_img, (T_y, T_x), 25, (0, 0, 255), 2) # manuly draw the first circle
video.write(old_img)

for i in range(2,N):
	name = image_name(i)
	img = cv2.imread(name)
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# cv2.imshow('img', img)
	# SSD(T_x,T_y,gold_img,img,gray_img)
	# CC(T_x,T_y,gold_img,img,gray_img)
	NCC(T_x,T_y,gold_img,img,gray_img)



cv2.waitKey(0)
cv2.destroyAllWindows()

