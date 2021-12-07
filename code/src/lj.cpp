#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <vector>
#include <omp.h>
#include "lj.h"

using std::vector;
using namespace std;

double minImage(double d, double b){
   return d - b*round(d/b);
}

double norm_3D(double x, double y, double z){
  return sqrt(dot_3D(x,y,z,x,y,z));
}

double dot_3D(double x1, double y1, double z1,
              double x2, double y2, double z2){
  return x1*x2 + y1*y2 + z1*z2;
}

void ljAA(double *xyz, double eps, double sig12, 
          double sig6, int nA, double *box, double &E)
{
  double dist, d2, d4, d6, d12, vx, vy, vz;

  E = 0.0;
#pragma omp parallel for default(none) shared(E,xyz,box,nA,sig12,sig6,eps) private(vx,vy,vz,dist,d2,d4,d6,d12)
  for(int n=0; n<nA; ++n)
     for(int m=0; m<n; ++m){

        vx = xyz[3*n]   - xyz[3*m];
        vy = xyz[3*n+1] - xyz[3*m+1];
        vz = xyz[3*n+2] - xyz[3*m+2];
        vx = minImage(vx, box[0]);
        vy = minImage(vy, box[1]);
        vz = minImage(vz, box[2]);

        dist = norm_3D(vx, vy, vz);
        d2 = dist*dist;
        d4 = d2*d2;
        d6 = d2*d4;
        d12 = d6*d6;

        E += eps*(sig12/d12 - sig6/d6);        
     }
 
}


void ljAB(double *xyzA, double *xyzB, double eps, double sig12, 
          double sig6, int nA, int nB, double *box, double &E)
{
  double dist, d2, d4, d6, d12, vx, vy, vz;

  E = 0.0;
#pragma omp parallel for default(none) shared(xyzA,xyzB,box,nA,nB,sig12,sig6,eps,E) private(vx,vy,vz,dist,d2,d4,d6,d12)
  for(int n=0; n<nA; ++n)
     for(int m=0; m<nB; ++m){

        vx = xyzA[3*n]   - xyzB[3*m];
        vy = xyzA[3*n+1] - xyzB[3*m+1];
        vz = xyzA[3*n+2] - xyzB[3*m+2];
        vx = minImage(vx, box[0]);
        vy = minImage(vy, box[1]);
        vz = minImage(vz, box[2]);

        dist = norm_3D(vx, vy, vz);
        d2 = dist*dist;
        d4 = d2*d2;
        d6 = d2*d4;
        d12 = d6*d6;

        E += eps*(sig12/d12 - sig6/d6);        
 
     }

}

