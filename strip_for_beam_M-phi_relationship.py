
# coding: utf-8

# In[ ]:


import numpy as np

def concrete(c_strain):
    ##混凝土本构
    if c_strain <= 0:     ## 未考虑混凝土受拉
        c_stress = 0;
    elif c_strain >= 0.002:
        c_stress = 23;    ##受压为正
    else:
        c_stress = 23 * (2 * c_strain / 0.002 - (c_strain / 0.002)**2)
    return c_stress;

def steel(s_strain):
    ##钢筋本构
    if s_strain <= -0.0018:
        s_stress = -357;  ## 受拉为负
    elif s_strain >= 0.0018:
        s_stress = 357;
    else:
        s_stress = 2e5 * s_strain
    return s_stress;
## 给定p 和 phi 求 轴力  
def Force(p,phi):
    s_strain = (steel_y - p) * phi
    s_stress = steel(s_strain)
    Fs = 0
    Fs = As * s_stress        
    Ms = 0
    Ms = Fs * (steel_y - p)   ## 弯矩逆时针为正   对中和轴处求矩

    Fc = 0
    Mc = 0
    for j in range(len(concrete_y)):
        c_strain = (concrete_y[j] - p) * phi
        c_stress = concrete(c_strain)
        Fc_strip = c_stress * b * width
        Fc = Fc + Fc_strip
        Mc = Mc + Fc_strip * (concrete_y[j] - p)
    N = Fc + Fs
    M = Ms + Mc
    return N
##给定 p 和 phi 求弯矩
def M(p,phi):
    s_strain = (steel_y - p) * phi
    s_stress = steel(s_strain)
    Fs = 0
    Fs = As * s_stress
    Ms = 0
    Ms = Fs * (steel_y - p)   ## 弯矩逆时针为正   对中和轴处求矩

    Fc = 0
    Mc = 0
    for j in range(len(concrete_y)):
        c_strain = (concrete_y[j] - p) * phi
        c_stress = concrete(c_strain)
        Fc_strip = c_stress * b * width
        Fc = Fc + Fc_strip
        Mc = Mc + Fc_strip * (concrete_y[j] - p)
    N = Fc + Fs
    M = Ms + Mc
    return M
## 找到正确的受压区高度 x：x = h/2 - p 
def erfen(aa,bb):
    cc = (aa + bb)/2
    fa = Force(aa,phi)
    fb = Force(bb,phi)
    fc = Force(cc,phi)
    while (abs(fc)> 100):     ## 当轴力N小于100牛 认为N = 0 满足平衡条件 
        if fa* fc < 0:
            bb = cc
        else :
            aa = cc
        cc = (aa + bb)/2
        fa = Force(aa,phi)
        fb = Force(bb,phi)
        fc = Force(cc,phi)
    p = cc   
    return p

h = 600    ##梁高
b = 250    ##梁宽
s_d = 22   ##受拉钢筋直径
s_n = 2    ##受拉钢筋数
As = 3.14 * (s_d ** 2) / 4 * s_n   ##受拉钢筋面积
width = 20   ##条带宽度
c = 25     ##保护层厚度
## 混凝土条带的位置 受压是正方向 受拉为负方向
concrete_y = np.arange(-(h/2-width/2),(h/2+width/2),width);
##钢筋位置
steel_y = -(h/2-c-s_d/2)
## phi取值范围
phi_range = np.arange(0,9e-5,1e-6)
for i in range(len(phi_range)):
    phi = phi_range[i]
    pp = erfen(0,h/2)         ## 找正确的p 上下限取为 0 h/2 
    judge = (concrete_y[len(concrete_y)-1] - pp) * phi
    if judge <= 0.0033:    ##如果混凝土受拉边缘大于混凝土极限压应变0.0033，输出-1
        wanju = M(pp,phi)/1e6
        print(phi,wanju)
    else:
        print(phi,-1)


