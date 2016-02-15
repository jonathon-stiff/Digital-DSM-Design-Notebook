# Import numerical function library
from numpy import floor, array, log2, mean, int

# Import scientific:signal function library
from scipy.signal import welch

#
# Function: Power spectral density using Welchs method
#
def psd_welch(invec,fs=1,seg=8):
    # Set start and end of data sequence
    nend=len(invec)
    olen=2**int(floor(log2(nend)))
    nstart=nend-olen
    if (nstart<0) : nstart=0

    # Obtain zero mean input sequence
    xout=array(invec)
    out=xout[nstart:nend]-mean(xout[nstart:nend])

    # Set FFT lengths
    nfft1=int(olen)
    nfft2=int(floor(nfft1/seg))

    # Set number of overlap sections
    noverlap1=int(0)
    noverlap2=int(nfft2*(2**-1))
    
    # Generate PSD using welch method
    fp1, Pxx1 = welch(out, fs,
                      window='hann',
                      nperseg=nfft1, 
                      noverlap=noverlap1,
                      return_onesided=False,
                      scaling='density'
                     )

    fp2, Pxx2 = welch(out, fs,
                      window='hann',
                      nperseg=nfft2, 
                      noverlap=noverlap2,
                      return_onesided=False,
                      scaling='density'
                     )
    
    # Return frequency and psds
    return fp1,fp2,Pxx1,Pxx2

