from phue import Bridge
from pprint import pprint
import time
import re
import asyncio


# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
#b.connect()
# Get the bridge state (This returns the full dictionary that you can explore)
#pprint(b.get_api())


def get_bridge(ip):
    return Bridge(ip)


def get_lights_dict(bridge):
    return bridge.get_light_objects('id')


def get_lights_list(bridge):
    return bridge.lights


def filter_lights_list(lights, keyword):
    """Filter a list of lights by a keyword in their name.
    """
    newLights = []
    for l in lights:
        if re.search(keyword, l.name):
            newLights.append(l)
    return newLights


def toggle_light(light):
    light.on = False if light.on else True


def set_light_saturation(light, value):
    light.saturation = value


def set_light_brightness(light, value):
    light.brightness = value


async def rotate_hue(light, start):
    light.hue = start
    while True:
        for i in range(start,65534,250):
            print(i)
            await asyncio.sleep(0.15)
            light.hue = i
        start = 1


async def breathe(light, min_bri = 1, max_bri = 254, step = 2, wait = 0.15):
    # TODO Error Handling
    print('Breathing Light: {}'.format(light.name))
    print('Min Brightness: {}'.format(min_bri))
    print('Max Brightness: {}'.format(max_bri))
    print('Step Value: {}'.format(step))
    print('Wait Value: {}'.format(wait))
    light.brightness = 1
    start = min_bri
    while True:
        for i in range(min_bri,max_bri,step):
            print(i)
            await asyncio.sleep(wait)
            light.brightness = i       
        step *= -1
        for i in range(max_bri,min_bri,step):
            print(i)
            await asyncio.sleep(wait)
            light.brightness = i
        step *= -1


async def rotate_saturation(light, start):
    light.saturation = start
    while True:
        for i in range(start,254,2):
            print(i)
            await asyncio.sleep(0.15)
            light.saturation = i
        start = 1


async def main():
    bridge = get_bridge('192.168.1.93')
    allLights = get_lights_list(bridge)
    lights = filter_lights_list(allLights, 'strip')
    lights += filter_lights_list(allLights, 'Lamp')

    tasks = []
    for l in allLights:
        print(l.brightness)
        task = asyncio.create_task(breathe(l, 10, 254, 10, 0.2))
        tasks.append(task)

    for t in tasks:
        await t


if __name__ == '__main__':
    asyncio.run(main())
