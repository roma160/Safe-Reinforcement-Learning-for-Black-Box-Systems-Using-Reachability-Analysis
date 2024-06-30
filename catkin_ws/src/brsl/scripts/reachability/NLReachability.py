from .Zonotope import Zonotope
from .MatZonotope import MatZonotope
import numpy as np 
from .utils.Options import Options
from .utils.Params import Params
from .reachability_nonlinear import *
import time
import os

class NLReachability:
    """
    This class is used to perform reachability analysis on a non linear system.
    """

    def __init__(self, path=""):
        self.dim_x = 2
        self.dim_u = 8
        self.dim_pose = self.dim_u
        self.dim_a = 2

        self.dt = 0.015
        self.params = Params(tFinal = self.dt * 5, dt = self.dt)

        self.options = Options()
        self.options.params["dim_x"] = self.dim_x
        self.options.params["dim_u"] = self.dim_u
        
        #Number of trajectories
        self.initpoints = 1000
        #Number of time steps
        self.steps = 10

        # Total number of samples
        self.totalsamples = 500 #steps * initpoints

        #noise zonotope
        self.wfac = 0.001

        self.W = Zonotope(
            np.array(np.zeros((self.options.params["dim_x"], 1))),
            self.wfac * np.ones((self.options.params["dim_x"], 1))
        )
        self.params.params["W"] = self.W
        
        self.GW = []
        for i in range(self.W.generators().shape[1]):
            vec = np.reshape(self.W.Z[:, i + 1], (self.dim_x, 1))
            dummy = []
            dummy.append(np.hstack((vec, np.zeros((self.dim_x, self.totalsamples - 1)))))
            #print(vec.shape, W.Z.shape, dummy[i][:, 2:].shape, dummy[0][:, 0].shape)
            for j in range(1, self.totalsamples, 1):
                right = np.reshape(dummy[i][:, 0:j], (self.dim_x, -1))
                left = dummy[i][:, j:]
                dummy.append(np.hstack((left, right)))
            self.GW.append(np.array(dummy))

        self.GW = np.array(self.GW[0])
        self.params.params["Wmatzono"] = MatZonotope(np.zeros((self.dim_x, self.totalsamples)), self.GW)

        self.options.params["zonotopeOrder"] = 100
        self.options.params["tensorOrder"] = 2
        self.options.params["errorOrder"] = 5

        self.u = np.load(os.path.join(path, 'uclean.npy'), allow_pickle=True)
        self.x_meas_vec_0 = np.load(os.path.join(path, 'X0_clean.npy'), allow_pickle=True)
        self.x_meas_vec_1 = np.load(os.path.join(path, 'X1clean.npy'), allow_pickle=True)
        self.X_0T = self.x_meas_vec_0
        self.X_1T = self.x_meas_vec_1
        self.options.params["U_full"] = self.u

        L = 0
        for i in range(self.totalsamples):
            z1 = np.hstack((self.x_meas_vec_0[:, i].flatten(), self.u.flatten(order='F')[i]))
            f1 = self.x_meas_vec_1[:, i]
            for j in range(self.totalsamples):
                z2 = np.hstack((self.x_meas_vec_0[:, j].flatten(), self.u.flatten(order='F')[j]))
                f2 = self.x_meas_vec_1[:, j]
                new_norm = np.linalg.norm(f1 - f2) / np.linalg.norm(z1 - z2)

                if (new_norm > L):
                    L = new_norm
                    eps = L * np.linalg.norm(z1 - z2)
        
        print("got here", L)
        self.options.params["Zeps"] = Zonotope(np.array(np.zeros((self.dim_x, 1))),eps * np.diag(np.ones((self.options.params["dim_x"], 1)).T[0]))
        self.options.params["ZepsFlag"] = True
        self.options.params["Zeps_w"] = self.params.params["W"] + self.options.params["Zeps"]
        self.options.params["X_0T"] = self.x_meas_vec_0
        self.options.params["X_1T"] = self.x_meas_vec_1 

    def run_reachability(self, r = [0, 0, 0, 0], u = [0, 0]):
        R0 = Zonotope(np.array(r).reshape((self.dim_x, 1)), np.diag([.001] * self.dim_x))
        self.params.params["R0"] = R0
        R_data, derivatives = self.reach_DT(self.params, self.options, u)
        return R_data, derivatives


    def reach_DT(self, params, options, u, *varargin):
        options = self.params2options(params,options)
        steps = len(u)#len(t) - 1
        R_data = [params.params["R0"]]
        derivatives = []
        for i in range(steps):
            if('uTransVec' in options.params):
                options.params['uTrans'] = options.params["uTransVec"][:, i]
            U = Zonotope(np.array(np.array(u[i]).reshape((self.dim_u, 1))), np.diag([.001] * self.dim_u))
            self.params.params["U"] = U
            uTrans = U.center()
            self.options.params["U"] = U  - uTrans
            self.options.params["uTrans"] = uTrans

            new_state, dc_dr, dc_du = self.linReach_DT(R_data[i] ,options)
            R_data.append(new_state.reduce('girard', 1))
            derivatives.append([dc_dr, dc_du])
        return R_data, derivatives

    def params2options(self, params, options):
        for key, value in params.params.items():
            options.params[key] = value
        return options 


    def set_inputSet(self, options):
        """
        This function is greatly modified and different from the one in CORA. 
        Mostly removed parts that are irrelevant to our reachability analysis techniques, that is the check for "checkOptionsSimulate"
        """
        uTrans = options.params["U"].center()
        options.params["U"] = options.params["U"]  - uTrans
        options.params["uTrans"] = uTrans
        return options


    def checkOptionsReach(self, options, hyb):
        return options


    def linReach_DT(self, R_data ,options):
        """
        This function calculates teh next state for the reachability analysis of a non linear system.
        """
        options.params["Uorig"] = options.params["U"] + options.params["uTrans"]
        xStar = R_data.center()
        uStar = options.params["Uorig"].center()

        xStarMat = matlib.repmat(xStar, 1, options.params["X_0T"].shape[1])
        uStarMat  = matlib.repmat(uStar, 1, options.params["U_full"].shape[1])
        oneMat    = matlib.repmat(np.array([1]), 1, options.params["U_full"].shape[1])
        num_mat = np.vstack([oneMat, options.params["X_0T"] + (-1 * xStarMat), options.params["U_full"] + -1 * uStarMat])
        IAB = np.dot(options.params["X_1T"], pinv(num_mat))
        V =  -1 * (options.params["Wmatzono"] + np.dot(IAB, num_mat)) + options.params["X_1T"]
        VInt = V.interval_matrix()
        leftLimit = VInt.Inf
        rightLimit = VInt.Sup
        V_one = Zonotope(Interval(leftLimit.min(axis=1).T, rightLimit.max(axis=1).T))
        x = R_data+(-1*xStar)
        result = (x.cart_prod(options.params["Uorig"] + (-1 * uStar)).cart_prod([1]) * IAB) +  V_one + options.params["Zeps_w"]
        return result, IAB[:self.dim_x, 1: 1 + self.dim_x], IAB[:self.dim_x, 1 + self.dim_x: 1 + self.dim_x + self.dim_a]