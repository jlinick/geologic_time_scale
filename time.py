#!/usr/bin/env python3
import math
import copy
import random
import numpy as np
import svgwrite
import data
import matplotlib.cm

# global variables (can change these)
white_background = False # white or black background
matplotlib_color = 'rainbow'#'gist_rainbow'#'cool'
linear_scale = False # if False, will use scale_factor to make the timeline logarithmic
scale_factor = 0.3# goes from 0-1. 0 is logarithmic, 1 is linear.
max_year = 4540. # oldest time
buff = (100,100,50,75) # buffer around image in pixels, (left, right, top, bottom)
xlen = 12000 # width in pix
ylen = 2000 # height in pix

# dicts for adjusting heights, etc
era_heights = {'supereon':100, 'eon':100, 'era':100, 'period':400, 'epoch':300, 'age':100}
era_sizes = {'supereon':70, 'eon':70, 'era':50, 'period':45, 'epoch':40, 'age':30} # font sizes
vertical_text = ['period', 'epoch'] # which eras to draw vertically
type_colors = {'general': [42,42,165], 'man': [127,0,255], 'extinction': [240,20,20], 'life': [20,210,20], 'geologic': [165,164,49], 'glac':[0,0,255]} # colors for event lines

# ignorable stuff
hh = [10,20,30] #used in generating allowed heights for range events
jj = 1 # used in generating heights

class abin:
    def __init__(self, name, start, height):
        self.name = name
        self.start = start
        self.height = height

def get_pix(year, linear=linear_scale, n=scale_factor):
    '''converts the year into a pixel number. If non-linear it goes from 1 (linear) to 0 (log)'''
    num_pix = xlen - buff[0] - buff[1]
    if linear:
        return buff[0] + (max_year - year) * num_pix / max_year # currently linear
    # log plot
    if year == max_year:
        return buff[0]
    #dist = math.log(year+1,n)/math.log(max_year+1,n)*num_pix
    x = year+1
    xm = max_year+1
    d = (x**n * math.log(x)) / (xm**n * math.log(xm))
    pix_num = xlen -buff[1] - d * num_pix
    return pix_num

def get_ypix(year):
    #determines the maximum y value for that year
    ti = copy.copy(data.allowed_times)
    ti.reverse()
    for tim in ti:
        objs = data.t.get_list(tim)
        for obj in objs:
             if year <= obj.start and year >= obj.end:
                 #determine height of eon
                 height = get_height(obj.typ)
                 return height

def get_height(eon):
    height = ylen - buff[3] - 100 # timeline height is 100
    for tim in data.allowed_times:
        height -= era_heights[tim]
        if tim == eon:
            return height
    return height

def get_range_height():
    global jj
    height = hh[jj%len(hh)]
    jj += 1
    return height

def get_color(obj):
    '''gets a color for a timeline object'''
    t = (obj.start + obj.end)/2
    ti = t/max_year
    cmap = matplotlib.cm.get_cmap(matplotlib_color)
    (r,g,b,a) = cmap(ti)
    color = 'rgb({},{},{})'.format(int(255*r),int(255*g),int(255*b))
    return color

def get_event_color(obj):
    lst = type_colors[obj.typ]

    #(r,g,b) = [int(np.clip(x + random.randint(-20, 20),0,255)) for x in lst]
    (r,g,b) = [int(np.clip(x,0,255)) for x in lst]
    color = 'rgb({},{},{})'.format(r,g,b)
    return color

def draw_obj(dwg, obj, abin):
    '''draws the object (rectangle if time)'''
    if type(obj) is time:
        draw_t(dwg, obj, abin)

def draw_t(dwg, obj, bn):
    '''draws the object in the appropriate bin'''
    x_min = get_pix(obj.start) 
    x_max = get_pix(obj.end)
    y_max = bn.start
    y_min = bn.start - bn.height
    color = get_color(obj)
    dx = x_max - x_min
    dy = y_max - y_min
    dwg.add(dwg.rect((x_min, y_min),(dx,dy), fill=color, stroke=svgwrite.rgb(10, 10, 10)))
    #print('{}: xmin:{} xmax:{} ymin{}, ymax:{}'.format(obj.name, x_min,x_max, y_min, y_max))
    x_avg = (x_min + x_max) / 2
    y_avg = (y_min + y_max) / 2
    fontsize = era_sizes[obj.typ.lower()]
    fontstr = '{}px'.format(fontsize)
    dx = len(str(obj.name.upper())) * fontsize /3.
    if obj.typ in vertical_text:
        label = obj.name.upper()
        rot = 'rotate(-90, {},{})'.format(x_avg, y_avg)
        textg = svgwrite.container.Group(transform=rot)
        textg.add(dwg.text(obj.name.upper(), insert=(x_avg, y_avg), fill='black', font_size=fontstr, text_anchor="middle", font_family='Times'))
        dwg.add(textg)
        #dwg.add(dwg.text(obj.name.upper(), insert=(x_avg - dx, y_avg+10), fill='black', font_size='30px', font_weight='bold', rotate=[90]))
    else:
        dwg.add(dwg.text(obj.name.upper(), insert=(x_avg - dx, y_avg+fontsize/3), fill='black', font_size=fontstr, font_weight='bold'))

def draw_all_the_things(dwg, t):
    '''draws all the timeline info'''
    curr_pos = ylen - buff[3]
    b = abin('timeline', curr_pos, 100)
    draw_tl(dwg,b)
    curr_pos -= b.height
    for period in data.allowed_times:
        objs = t.get_list(period)
        if len(objs) < 1:
            continue
        height = era_heights[period]
        b = abin(period, curr_pos, height)
        if period.lower() != 'supereon':
            draw_labels(dwg, b, period, t)
        for obj in objs:
            draw_t(dwg, obj, b)
        curr_pos -= height
    #draw events
    b = abin('events', curr_pos, 500)
    draw_title(dwg)
    draw_events(dwg, b, t)

def draw_labels(dwg, b, period, t):
    '''draws the eon/era labels'''
    # determine the x,y position
    y = b.start - b.height/2
    #determine left edge
    objs = t.get_list(period)
    fontsize = 40#era_sizes[period]
    x = get_pix(max([obj.start for obj in objs])) - fontsize/2
    textcolor = 'grey'
    if white_background == True:
        textcolor = 'grey'
    rot = 'rotate(-90, {},{})'.format(x, y)
    textg = svgwrite.container.Group(transform=rot)
    textg.add(dwg.text(period.upper(), insert=(x, y), fill=textcolor, font_size='{}px'.format(fontsize), font_weight='bold', text_anchor="middle", font_family='Times'))
    dwg.add(textg)


def draw_tl(dwg, b):
    '''draws the black timeline in the bin b'''
    # draw black line
    thickness = 5
    y = b.start - b.height + thickness-1
    dy = b.height
    xmin = get_pix(max_year)
    xmax = get_pix(0)
    linecolor = 'white'
    if white_background == True:
        linecolor = 'black'

    dwg.add(dwg.line( (xmin, y), (xmax,y), color=linecolor, stroke=linecolor, stroke_width=8))
    draw_hatch(dwg, y, 75, 15, 1000, draw_text=True)
    draw_hatch(dwg, y, 50, 7, 100, draw_text=True)
    draw_hatch(dwg, y, 40, 1, 10, draw_text=True)
    draw_hatch(dwg, y, 20, 1, 1)

def draw_hatch(dwg, y, height, thickness, div, draw_text=False):
    # draw hatch marks
    years = [x for x in  range(0,int(max_year),1) if (x%div == 0 and x%(div*10) !=0)]
    textcolor = 'white'
    if white_background == True:
        textcolor = 'black'
    if div == 1000:
        years.extend([0,max_year])
    font_size = '30px'
    for yr in years:
        xpos = get_pix(yr)
        dwg.add(dwg.line( (xpos, y-thickness/2+3.2), (xpos,y+height), color=textcolor, stroke=textcolor, stroke_width=thickness))
        if draw_text and div >= 100:
            yr_str = data.cvt_num(yr)
            dx = len(yr_str) * 8.
            if div == 1000:
                font_size = '40px'
                if yr_str == '0':
                    yr_str = '0 Ma.'
                    dx = 30
                dwg.add(dwg.text(yr_str, insert=(xpos - dx*1.4, y+height+40), fill=textcolor, font_size=font_size, font_weight='bold'))
            else:
                dwg.add(dwg.text(yr_str, insert=(xpos - dx, y+height+30), fill=textcolor, font_size=font_size, font_weight='bold'))
        elif (draw_text and yr%20 ==0 and yr < 100) or (yr in [1, 3, 5,7, 10]):
            yr_str = data.cvt_num(yr)
            dx = len(yr_str) * 8.
            dwg.add(dwg.text(yr_str, insert=(xpos - dx, y+height+30), fill=textcolor, font_size='30px', font_weight='bold'))

def draw_events(dwg, bn, t):
    events = calc_shifts(t.get_events_list())
    for event in events:
        # range events
        if event.start or event.end:
            draw_range_event(dwg, bn, t, event)
        else:
            draw_single_event(dwg, bn, t, event)

def draw_single_event(dwg, bn, t, event):
        # single event
        yr = event.t
        label = '{} Ma. {}'.format(data.cvt_num(event.t), event.name)
        x = get_pix(yr)
        dy = 120
        #y = bn.start-dy - 5
        y = get_ypix(yr) - 10 - dy
        # draw the line
        color = get_event_color(event)
        dwg.add(dwg.line((x+event.shift,y),( x, y+dy), stroke=color, stroke_width=5))
        #create_arrow_marker(dwg, (x,y), (x, y+dy))
        # place the text
        event_fontsize = 24
        #dx = len(label) * event_fontsize /3.
        dx = event_fontsize
        textcolor = 'white'
        if white_background == True:
            textcolor = 'black'
        #dwg.add(dwg.text(label, insert=(x+dx, y-30), fill='black', font_size='{}px'.format(event_fontsize)))
        rot = 'rotate(-90, {},{})'.format(x+5+event.shift, y-10)
        textg = svgwrite.container.Group(transform=rot)
        textg.add(dwg.text(label, insert=(x+5+event.shift, y-10), fill=textcolor, font_size='{}px'.format(event_fontsize), text_anchor="start", font_family='Helvetica'))
        dwg.add(textg)

def draw_range_event(dwg,bn,t,event):
        yr = event.t
        start = event.start
        end = event.end
        label = '{} - {} Ma. {}'.format(data.cvt_num(event.start), data.cvt_num(event.end), event.name)
        x = get_pix(yr)
        xstart = get_pix(start)
        xend = get_pix(end)
        y1 = get_ypix(start)
        y2 = get_ypix(end)
        dy = get_range_height() #rand gap between lines
        y = min([y1,y2]) # height of the eon below 
        vline = 90 # height of vertical line
        gap = 10
        yh = [y, y-gap, y-gap-dy, y-gap-vline]
        thickness = 5
        color = get_event_color(event)
        # draw the lines
        dwg.add(dwg.line((x,yh[2]), (x, yh[3]), stroke=color, stroke_width=thickness))#vert line
        dwg.add(dwg.line((xstart, yh[2]), (xend, yh[2]), stroke=color, stroke_width=thickness))#horiz line
        #edge lines
        dwg.add(dwg.line((xstart,yh[2]-thickness/2), (xstart, yh[1]), stroke=color, stroke_width=thickness))
        dwg.add(dwg.line((xend,yh[2]-thickness/2), (xend, yh[1]), stroke=color, stroke_width=thickness))
        # place the text
        event_fontsize = 24
        dx = event_fontsize
        rot = 'rotate(-90, {},{})'.format(x+5, yh[3]-10)
        textg = svgwrite.container.Group(transform=rot)
        textcolor = 'white'
        if white_background == True:
            textcolor = 'black'
        textg.add(dwg.text(label, insert=(x+5, yh[3]-10), fill=textcolor, font_size='{}px'.format(event_fontsize), text_anchor="start", font_family='Helvetica'))
        dwg.add(textg)

def calc_shifts(events_list):
    '''add in small shifts left and right for events that overlap. returns the list'''
    allowable_range=25 #how close they are in pix
    for event in events_list:
        event.shift = 0
    for event in events_list:
        event_px = get_pix(event.t)
        for nearby_event in events_list:
            if nearby_event == event:
                continue
            nearby_px = get_pix(nearby_event.t)
            if abs(nearby_px - event_px) < allowable_range:
                shift = (nearby_px - event_px + allowable_range)/2
                event.shift -= shift
                nearby_event.shift += shift
    return events_list

def draw_title(dwg):
    title = 'Geologic Time Scale'
    fontsize = 150
    x = xlen/2
    y = fontsize/2 + 100 + buff[2]
    color = 'gray'
    if white_background == True:
        color = 'black'
    dwg.add(dwg.text(title, insert=(x, y), fill=color, font_size='{}px'.format(fontsize), text_anchor='middle', font_family='Times'))
    # add byline
    color = 'rgb(75,75,75)'
    if white_background == True:
        color = 'rgb(200,200,200)'
    x = xlen - 575
    y = ylen - 20
    byline = 'created by Justin Linick'
    dwg.add(dwg.text(byline, insert=(x, y), fill=color, font_size='20px', text_anchor='middle', font_family='Helvetica'))
    link =  'https://github.com/jlinick/geologic_time_scale'
    x = xlen - 250
    dwg.add(dwg.text(link, insert=(x, y), fill=color, font_size='20px', text_anchor='middle', font_family='Helvetica'))

if __name__ == '__main__':
    #load data
    t = data.t

    #instantiate object
    dwg = svgwrite.Drawing('timeline.svg', profile='tiny')
    #draw background
    color = 'black'
    if white_background == True:
        color = 'white'
    dwg.add(dwg.rect((0,0), (xlen, ylen), fill=color))

    #draw timeline, eras/eons/events/labels etc
    draw_all_the_things(dwg, t)

    # save
    dwg.save()

