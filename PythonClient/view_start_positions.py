#!/usr/bin/env python3

# Copyright (c) 2017 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Basic CARLA client example."""

from __future__ import print_function

import argparse
import logging
import random
import time

from carla.client import make_carla_client
from carla.sensor import Camera, Lidar
from carla.settings import CarlaSettings
from carla.tcp import TCPConnectionError
from carla.util import print_over_same_line

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle

def view_start_positions(args):



    # We assume the CARLA server is already waiting for a client to connect at
    # host:port. The same way as in the client example
    with make_carla_client(args.host, args.port) as client:
        print('CarlaClient connected')






        # We load the default settings to the client.
        scene = client.load_settings(CarlaSettings())
        print ("Receives the Start Position")



        # Notify the server that we want to start the episode at the
        # player_start index. This function blocks until the server is ready
        # to start the episode.

        from carla.planner.map import CarlaMap

        number_of_player_starts = len(scene.player_start_spots)
        if number_of_player_starts > 100:

            image = mpimg.imread("carla/planner/Town01.png")
            carla_map = CarlaMap('Town01', 0.1653, 50)

        else:

            image = mpimg.imread("carla/planner/Town02.png")
            carla_map = CarlaMap('Town02', 0.1653, 50)

        fig, ax = plt.subplots(1)

        ax.imshow(image)


        if args.positions == 'all':

            positions_to_plot = range(len(scene.player_start_spots))

        else:

            positions_to_plot = map(int, args.positions.split(','))



        for position in positions_to_plot:
            pixel = carla_map.convert_to_pixel([scene.player_start_spots[position].location.x
                                               , scene.player_start_spots[position].location.y
                                               , scene.player_start_spots[position].location.z])
            circle = Circle((pixel[0]
                             , pixel[1])
                            , 12, color='r')

            ax.add_patch(circle)

        plt.show()





def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='localhost',
        help='IP of the host server (default: localhost)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-pos', '--positions',
        metavar='P',
        default='all',
        help=' The positions that you want to plot on the map')




    args = argparser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    while True:
        try:

            view_start_positions(args)

            print('Done.')
            return

        except TCPConnectionError as error:
            import traceback
            traceback.print_exc()
            logging.error(error)
            time.sleep(1)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        import traceback
        traceback.print_exc()
        print('\nCancelled by user. Bye!')
