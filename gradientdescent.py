
""" Execute gradient descent on earth geometry """

import sys
import csv
import rasterio
import argparse
import numpy as np
from pylab import plot, show, xlabel, ylabel

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, default='output.csv')
parser.add_argument('--alpha', type=float, default=0.01)
parser.add_argument('--gamma', type=float, default=0.99)
parser.add_argument('--iters', type=int, default=1000)
parser.add_argument('lat', type=float)
parser.add_argument('lon', type=float)
parser.add_argument('tif', type=str)
args = parser.parse_args()

src = rasterio.open(args.tif)
band = src.read(1)

delta = 0.001



def get_elevation(lat, lon):
    vals = src.index(lon, lat)
    return band[vals]

def compute_cost(theta):
    lat, lon = theta[0], theta[1]
    J = get_elevation(lat, lon)
    return J

def gradient_descent_vanilla(theta, alpha, gamma, num_iters):
    J_history = np.zeros(shape=(num_iters, 3))
    velocity = [ 0, 0 ]

    for i in range(num_iters):
        cost = compute_cost(theta)

        # Fetch elevations at offsets in each dimension
        elev1 = get_elevation(theta[0] + delta, theta[1])
        elev2 = get_elevation(theta[0] - delta, theta[1])
        elev3 = get_elevation(theta[0], theta[1] + delta)
        elev4 = get_elevation(theta[0], theta[1] - delta)

        J_history[i] = [ cost, theta[0], theta[1] ]
        if cost <= 0: return theta, J_history

        # Calculate slope
        lat_slope = elev1 / elev2 - 1
        lon_slope = elev3 / elev4 - 1

        # Update variables
        theta[0][0] = theta[0][0] - alpha * lat_slope
        theta[1][0] = theta[1][0] - alpha * lon_slope

    return theta, J_history

def gradient_descent_momentum(theta, alpha, gamma, num_iters):
    J_history = np.zeros(shape=(num_iters, 3))
    velocity = [ 0, 0 ]
    for i in range(num_iters):

        cost = compute_cost(theta)

        elev1 = get_elevation(theta[0] + delta, theta[1])
        elev2 = get_elevation(theta[0] - delta, theta[1])
        elev3 = get_elevation(theta[0], theta[1] + delta)
        elev4 = get_elevation(theta[0], theta[1] - delta)

        J_history[i] = [ cost, theta[0], theta[1] ]
        if cost <= 0: return theta, J_history

        lat_slope = elev1 / elev2 - 1
        lon_slope = elev3 / elev4 - 1

        velocity[0] = gamma * velocity[0] + alpha * lat_slope
        velocity[1] = gamma * velocity[1] + alpha * lon_slope

        print('Update is', velocity[0])
        print('Update is', velocity[1])
        print('Elevation at', theta[0], theta[1], 'is', cost)

        theta[0][0] = theta[0][0] - velocity[0]
        theta[1][0] = theta[1][0] - velocity[1]

    return theta, J_history

def gradient_descent_adagrad(theta, alpha, gamma, num_iters):
    J_history = np.zeros(shape=(num_iters, 3))
    epsilon = 10 ** (-8)
    alpha_lst = [0, 0]
    for i in range(num_iters):

        cost = compute_cost(theta)

        elev1 = get_elevation(theta[0] + delta, theta[1])
        elev2 = get_elevation(theta[0] - delta, theta[1])
        elev3 = get_elevation(theta[0], theta[1] + delta)
        elev4 = get_elevation(theta[0], theta[1] - delta)

        J_history[i] = [ cost, theta[0], theta[1] ]
        if cost <= 0: return theta, J_history

        lat_slope = elev1 / elev2 - 1
        lon_slope = elev3 / elev4 - 1

        alpha_lst[0] += lat_slope ** 2
        alpha_lst[1] += lon_slope ** 2
        alpha_lat = alpha / np.sqrt(alpha_lst[0] + epsilon)
        alpha_lon = alpha / np.sqrt(alpha_lst[1] + epsilon)

        theta[0][0] = theta[0][0] - alpha_lat
        theta[1][0] = theta[1][0] - alpha_lon

    return theta, J_history

theta = np.array([ [args.lat], [args.lon] ])
theta, J_history = gradient_descent_vanilla(theta, args.alpha, args.gamma, args.iters)

theta2 = np.array([ [args.lat], [args.lon] ])
theta2, J_history2 = gradient_descent_momentum(theta2, args.alpha, args.gamma, args.iters)

theta3 = np.array([ [args.lat], [args.lon] ])
theta3, J_history3 = gradient_descent_adagrad(theta3, args.alpha, args.gamma, args.iters)


with open(args.output+"vanilla", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for weight in J_history:
        if weight[1] != 0 and weight[2] != 0:
            writer.writerow([ weight[1], weight[2] ])

plot(np.arange(args.iters), J_history[:, 0])
xlabel('Iterations')
ylabel('Elevation')
show()

with open(args.output+"momentum", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for weight in J_history2:
        if weight[1] != 0 and weight[2] != 0:
            writer.writerow([ weight[1], weight[2] ])

plot(np.arange(args.iters), J_history2[:, 0])
xlabel('Iterations')
ylabel('Elevation')
show()

with open(args.output+"adagrad", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for weight in J_history3:
        if weight[1] != 0 and weight[2] != 0:
            writer.writerow([ weight[1], weight[2] ])

plot(np.arange(args.iters), J_history3[:, 0])
xlabel('Iterations')
ylabel('Elevation')
show()
