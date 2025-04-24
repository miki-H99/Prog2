""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import numpy as npy 



def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here

    points = [(random.uniform(-1,1),random.uniform(-1,1)) for i in range(n)]
    ncx = []
    ncy = []
    
    nsx = []
    nsy = []
    for i in points:
        if i[0]**2 + i[1]**2 <= 1:
            ncx.append(i[0]) 
            ncy.append(i[1]) 
        else:     
            nsx.append(i[0]) 
            nsy.append(i[1]) 
        

    # print(len(ncx))
    pi_aprx = 4*(len(ncx)/n)
    print(f"Approximated π: {pi_aprx}")
    plt.figure()
    plt.scatter(ncx, ncy, color='red', label='Inside Circle', s=10)
    plt.scatter(nsx, nsy, color='blue', label='Outside Circle', s=10)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.title(f"Monte Carlo π Approximation (n={n})")
    plt.show()
    return pi_aprx

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 

    rand_points = [[random.uniform(-1, 1) for i in range(d)] for k in range(n)]

    radius = [ sum([i**2 for i in k]) for k in rand_points]
    inside = list(filter( lambda x: x <= 1 ,radius))
    ratio = len(inside)/len(radius) 
    Vaprox = ratio * (2**d) 

    return Vaprox


def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 

    numerator = m.pi**(d/2) 
    Vd = numerator/(m.gamma((d/2) + 1))

    return Vd

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np):
      #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    n_points = [n//np]*np #split the n-points accros n-process
    d_dims = np*[d] # np dimensions per each subset of n-points
    with future.ProcessPoolExecutor() as ex:
    

        result = list(ex.map(sphere_volume,n_points,d_dims))
    
    
    # length = len(result)
    
    mean_sphere = npy.mean(result)
    # print(f"length of results list: {length}")
    # print(n_points)
        # result = [ex.submit(sphere_volume,n,d) for _ in range(10)]
        # results = [ n.result() for n in future.as_completed(result)]
        # mean_sphere = mean(results)
    
     

    return mean_sphere

#Ex4: parallel code - parallelize actual computations by splitting data
def squared_radi (points):
        
        return [sum(d**2 for d in point) for point in points]  

def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    # ratio = n//np
    n_points_process = n//np # splita upp antalet punkter över processer np
    # d_dims = [d]*np
    
    rand_points =[[[random.uniform(-1, 1) for _ in range(d)] #do är alla dim-punkter per n-points
                        for _ in range(n_points_process)] # skapar n_points_process st d-dimensionella spheres
                      
                        for _ in range(np)] #för i np olika processer

    with future.ProcessPoolExecutor() as ex:
        # radius = [[ex.map( squared_radi,n_spheres)for n_spheres in n_set ] for n_set  in  rand_points]

        radiis = list(ex.map(squared_radi,rand_points)) # funktionens körs mot rand_points =  rand_points[0] per maping
        

    rads = list()
    for radis in radiis:
        for rad in radis:
            rads +=[rad]
    inside = list(ex.map(filter( lambda rad: rad <= 1 ,rads)))
    
    ratio = len(inside)/len(rads)

    Vaprox = ratio/(n * (2**d)) 
    return Vaprox
    
    
def main():
    #Ex1
     dots = [1000, 10000, 100000]
     for n in dots:
         approximate_pi(n)
    # #Ex2
    # n = 100000
    # d = 2
    # d2 = sphere_volume(n,d)
    # print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)},vs approximated = {d2} ")

    # n = 100000
    # d = 11
    # d11 = sphere_volume(n,d)
    # print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(d)}, vs approximated = {d11}")

    # #Ex3
    # n = 100000
    # d = 11
    # np = 10
    # start = pc()
    # spehere_vals  = []

    # for y in range (np):
    #     spehere_vals.append(sphere_volume(n,d))
    # stop = pc()
    # print(f"average sphere valoume: {mean(spehere_vals)}")
    # print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")

    # print("What is parallel time?")
    # start1 = pc()
    # average = sphere_volume_parallel1(n,d,np)

    # end1= pc()
    # print(f"The parell time is: {end1 - start1}")
    # print(f"the average sphere value : {average} ")
    #Ex4
    # n = 1000000
    
    #d = 11
    #start = pc()
    #sphere_volume(n,d)
    #stop = pc()
    #print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    #print("What is parallel time?")
    #starting = pc()
    #sphere_volume_parallel2(n,d)
    #ending  = pc()
    #print(f"Ex4: Parallel time of {d} and {n}: {ending-starting}")

    
    

if __name__ == '__main__':
	main()
