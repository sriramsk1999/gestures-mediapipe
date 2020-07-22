'''
Functions which implement code to track the mouse,
given a set of landmarks.
'''

def get_avg_pointer_loc(pointer_buffer):
    '''Gets average of previous 5 pointer locations'''
    x = [i[0] for i in pointer_buffer]
    y = [i[1] for i in pointer_buffer]
    return sum(x)/len(pointer_buffer), sum(y)/len(pointer_buffer)


def calc_pointer(landmarks, S, resolution):
    ''' Uses the landmarks to calculate the location of the cursor on the screen. '''

    # The tip of the index pointer is the eighth landmark in the list
    index_pointer = landmarks[8]['x'], landmarks[8]['y'], landmarks[8]['z']

    scaled_pointer = resolution[0]*index_pointer[0], resolution[1]*index_pointer[1]

    S.pointer_buffer.append(scaled_pointer)
    S.pointer_buffer.pop(0)
    actual_pointer = get_avg_pointer_loc(S.pointer_buffer)

    return actual_pointer, S


def mouse_track(current_pointer, S, mouse):
    '''
    Performs mouse actions depending on the S.flags that have been set.
    S.prev_pointer is only modified if the mouse is up and we are not scrolling.
    '''
    threshold = 100

    # If mouse is down and movement below threshold, do not move the mouse
    if S.mouse_flags['mousedown'] and (abs(current_pointer[0] - S.prev_pointer[0]) +
                                       abs(current_pointer[1] - S.prev_pointer[1]) < threshold):
        pass
    elif S.mouse_flags['scroll']:
        amt_to_scroll = (current_pointer[1] - S.prev_pointer[1])/10
        mouse.scroll(0, amt_to_scroll)
    else:
        mouse.position = current_pointer
        S.prev_pointer = current_pointer
    return S
