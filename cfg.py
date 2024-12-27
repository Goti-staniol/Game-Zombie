from pygame import image, transform

W, H = 700, 500
FPS = 30

player_img = 'src/images/player_sprite.png'


start_btn_img = 'src/images/b_imgs/start_btn.png'
hover_start_img = 'src/images/b_imgs/hover_start.png'

exit_btn_img = 'src/images/b_imgs/exit_btn.png'
hover_exit_img = 'src/images/b_imgs/hover_exit.png'

check_box_c = 'src/images/checkbox/checked.png'
check_box_u = 'src/images/checkbox/unchecked.png' 

bg_img = transform.scale(image.load('src/images/bg.png'), (W, H))

bullet_img = 'src/images/bullet.png'

idle = [
    image.load('src/images/p_idle/1.png'),
    image.load('src/images/p_idle/2.png')
]

walking = [
    image.load('src/images/p_walking/one.png'),
    image.load('src/images/p_walking/two.png'),
    image.load('src/images/p_walking/three.png'),
    image.load('src/images/p_walking/four.png'),
    image.load('src/images/p_walking/five.png'),
    image.load('src/images/p_walking/six.png')
    
]
