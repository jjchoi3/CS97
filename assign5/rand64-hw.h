
/* Description of the current CPU. */
struct cpuid { unsigned eax, ebx, ecx, edx; };

/* Return information about the CPU. */
struct cpuid cpuid (unsigned int leaf, unsigned int subleaf);

/* Return true if the CPU supports the RDRAND instruction.  */
_Bool rdrand_supported (void);


/* Initialize the hardware rand64 implementation.  */
void hardware_rand64_init (void);

/* Return a random value, using hardware operations.  */
unsigned long long hardware_rand64 (void);

/* Return a random value, using hardware operations (Alternate).  */
unsigned long long hardware_rand48(void);

/* Finalize the hardware rand64 implementation.  */
void hardware_rand64_fini (void);
