from pygame import image, transform

W, H = 700, 500
FPS = 30

start_btn_img = 'src/images/b_imgs/start_btn.png'
hover_start_img = 'src/images/b_imgs/hover_start.png'
exit_btn_img = 'src/images/b_imgs/exit_btn.png'
hover_exit_img = 'src/images/b_imgs/hover_exit.png'
bg_img = transform.scale(image.load('src/images/bg.png'), (W, H))

idle = [
    image.load('src/images/p_idle/1.png'),
    image.load('src/images/p_idle/2.png'),
    # image.load('images/p_idle/3.png')
]

walk_right = [
    image.load('src/images/p_right/one.png'),
    image.load('src/images/p_right/two.png'),
    image.load('src/images/p_right/three.png'),
    image.load('src/images/p_right/four.png'),
    image.load('src/images/p_right/five.png'),
    image.load('src/images/p_right/six.png')
    
]

walk_left = [
    image.load('src/images/p_right/one.png'),
    image.load('src/images/p_right/two.png'),
    image.load('src/images/p_right/three.png'),
    image.load('src/images/p_right/four.png'),
    image.load('src/images/p_right/five.png'),
    image.load('src/images/p_right/six.png')
]