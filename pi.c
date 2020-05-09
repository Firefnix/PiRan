#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>

#define DIGITS_PER_ITERATION 14.1816474627254776555
#define LOG_2_10  3.32192809488736234789

/*
 * gcc -O2 -shared -Wl,-soname,pi -o pi.so -fPIC pi.c -lgmp
 */

char *pi_str(unsigned long digits) {
	mpf_t result, con, A, B, F, sum;
	mpz_t a, b, c, d, e;
	char *output;
	mp_exp_t exp;

	unsigned long int k, threek;
	unsigned long iterations = (digits/DIGITS_PER_ITERATION)+1;

	mpf_set_default_prec((digits *LOG_2_10) + 1);

	mpf_inits(result, con, A, B, F, sum, NULL);
	mpz_inits(a, b, c, d, e, NULL);

	// first the constant sqrt part
	mpf_sqrt_ui(con, 10005);
	mpf_mul_ui(con, con, 426880);

	for (k = 0; k < iterations; k++) {
		threek = 3*k;

		mpz_fac_ui(a, 6*k);  // (6k)!

		mpz_set_ui(b, 545140134); // 13591409 + 545140134k
		mpz_mul_ui(b, b, k);
		mpz_add_ui(b, b, 13591409);

		mpz_fac_ui(c, threek);  // (3k)!

		mpz_fac_ui(d, k);  // (k!)^3
		mpz_pow_ui(d, d, 3);

		mpz_ui_pow_ui(e, 640320, threek); // -640320^(3k)
		if ((threek&1) == 1)
			mpz_neg(e, e);

		// numerator (in A)
		mpz_mul(a, a, b);
		mpf_set_z(A, a);

		// denominator (in B)
		mpz_mul(c, c, d);
		mpz_mul(c, c, e);
		mpf_set_z(B, c);

		// result
		mpf_div(F, A, B);

		// add on to sum
		mpf_add(sum, sum, F);
	}

	mpf_ui_div(sum, 1, sum); // invert result
	mpf_mul(sum, sum, con); // multiply by constant sqrt part

	// get result base-10 in a string:
	output = mpf_get_str(NULL, &exp, 10, digits, sum); // calls malloc()

	mpf_clears(result, con, A, B, F, sum, NULL);
	mpz_clears(a, b, c, d, e, NULL);

	return output;
}

void free_string(char *ptr) {
	free(ptr);
}
