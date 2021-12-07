#ifndef _LJ_H_
#define _LJ_H_
#ifdef __cplusplus
extern "C" {
#endif

double minImage(double d, double b);

double norm_3D(double x, double y, double z);

double dot_3D(double x1, double y1, double z1,
              double x2, double y2, double z2);

void ljAB(double *xyzA, double *xyzB, double eps, 
            double sig12, double sig6, int nA, int nB, 
            double *box, double &EAB);

void ljAA(double *xyz, double eps, double sig12, 
            double sig6, int nA, double *box, double &EAA);

#ifdef __cplusplus
}
#endif
#endif
