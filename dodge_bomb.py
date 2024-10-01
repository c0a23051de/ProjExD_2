import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct):
    """
    引数：こうかとん　または　爆弾のRCT
    戻り値：真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue　画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko,tate
def game_over(screen:pg.rect) -> tuple[bool]:
    """
    引数：こうかとんと爆弾がぶつかったときの背景
    """
    black_scr = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_scr, (0, 0, 0), black_scr.get_rect())
    black_scr.set_alpha(180)
    screen.blit(black_scr, (0, 0))

    kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = WIDTH/2+180, HEIGHT/2
    screen.blit(kk_img, kk_rct)
    kk_rct.center = WIDTH/2-180, HEIGHT/2
    screen.blit(kk_img, kk_rct)

    font = pg.font.Font(None, 80)  # フォント
    gameover_font = font.render("Game Over", True, (255,255, 255))  # 白で描画
    gameover_rct = gameover_font.get_rect()
    gameover_rct.center = WIDTH / 2, HEIGHT / 2 
    screen.blit(gameover_font, gameover_rct)

    pg.display.update()  

    time.sleep(5) 


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))  # からのSurface
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)
    vx,vy = +5, -5
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)

    # bb2_img = pg.Surface((20,20))  # からのSurface
    # bb2_img.set_colorkey((0, 0, 0))
    # pg.draw.circle(bb2_img, (255,0,255), (10,10), 10)
    # vx2,vy2 = +5, -5
    # bb2_rct = bb2_img.get_rect()  # 爆弾Rectの抽出
    # bb2_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾がぶつかっていたら
           game_over(screen)
           return
        # if kk_rct.colliderect(bb2_rct):  # こうかとんと爆弾がぶつかっていたら
        #    game_over(screen)
        #    return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 横座標、縦座標
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横座標
                sum_mv[1] += tpl[1]  # 縦座標
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct ) != (True,True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(100)
        
        # bb2_rct.move_ip(vx2, vy2)
        # yoko, tate = check_bound(bb2_rct)
        # if not yoko:
        #     vx2 *= -1
        # if not tate:
        #     vy2 *= -1
        # screen.blit(bb2_img, bb2_rct)
        # pg.display.update()
        # tmr += 1
        # clock.tick(100)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
