import utime

def timed_function_us(f, *args, **kwargs):
    f_name = str(f).split(' ')
    myname = ""
    if len(f_name) > 1:
        myname = f_name[1]
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func