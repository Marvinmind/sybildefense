__author__ = 'Martin'
import pyopencl as cl
import numpy as np
import numpy.linalg as la
from time import clock

def mult(matrix1, matrix2):
	ctx = cl.create_some_context()
	queue = cl.CommandQueue(ctx)

	mf = cl.mem_flags
	a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix1)
	b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=matrix2)
	dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, matrix1.nbytes )


	prg = cl.Program(ctx, """
		__kernel void multiplymatrices(const unsigned int size, __global float * matrix1, __global float * matrix2, __global float * res) {

		int i = get_global_id(1);
		int j = get_global_id(0);

		res[i + size * j] = 0;

		for (int k = 0; k < size; k++)
		{
			res[i + size * j] += matrix1[i + size * k] * matrix2[k + size * j];
		}

		}
		""").build()

	t0 =clock()

	prg.multiplymatrices(queue, matrix1.shape, None,np.int32(len(matrix1)) ,a_buf, b_buf, dest_buf)

	final_matrix = np.empty_like(matrix1)
	cl.enqueue_copy(queue, final_matrix , dest_buf)

	print(final_matrix)


	delta_t = clock() - t0
	print('OpenCL Multiplication: ' + str(delta_t))

	return final_matrix

a = np.array([[1,2],[2,3]])
b = np.array([[1,2],[2,3]])

mult(a,b)