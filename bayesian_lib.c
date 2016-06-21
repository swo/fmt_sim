#include <math.h>
#include <stdio.h>

double pow(double x, double y);

double f(int n, double args[n]) {
    double product = 1.0;
    int donor_i;
    int history_i;
    double si;
    double fi;

    // unpack arguments
    double gamma = args[0];
    double beta = args[1];
    double phi = args[2];
    double epsilon = gamma + beta - gamma * beta;

    int n_donors = (int)args[3];

    for(donor_i=0; donor_i < n_donors; donor_i++) {
        // where is the successes for this donor?
        history_i = 2 * donor_i + 4;
        si = args[history_i];
        fi = args[history_i + 1];

        product *= phi * pow(epsilon, si) * pow((1.0 - epsilon), fi) + (1.0 - phi) * pow(beta, si) * pow((1.0 - beta), fi);
    }

    return product;
}
