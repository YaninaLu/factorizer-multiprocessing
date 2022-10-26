from multiprocessing import Pool, cpu_count, Manager
from itertools import repeat


def factorize_evens_odds(num):
    """
    Returns a list of all divisors of the given number.
    :param num: a number to factorize
    :return: list of divisors
    """
    res = [1]
    for i in range(2, num):
        if num % i == 0:
            res.append(i)
    res.append(num)
    return res


def factorize_odds(num):
    """
    Returns a list of all divisors of the given number provided that this number is not divisible by 2 and thus
    by any even number.
    :param num: a number to factorize
    :return: a list of divisors
    """
    res = [1]
    for i in range(3, num, 2):
        if num % i == 0:
            res.append(i)
    res.append(num)
    return res


def factorize_num(num, results):
    """
    Sorts numbers according to their divisibility by 2 and sends them to the corresponding function. Saves the results
    to the shared memory.
    :param num: a number to factorize
    :param results: a shared dict
    """
    if num % 2 == 0:
        res = factorize_evens_odds(num)
        results[num] = res
    else:
        res = factorize_odds(num)
        results[num] = res


def wrapper(args):
    return factorize_num(*args)


def main(arr):
    manager = Manager()
    results = manager.dict()

    with Pool(cpu_count()) as process_pool:
        process_pool.map(wrapper, zip(arr, repeat(results)))
        process_pool.close()
        process_pool.join()

    assert results[128] == [1, 2, 4, 8, 16, 32, 64, 128]
    assert results[255] == [1, 3, 5, 15, 17, 51, 85, 255]
    assert results[99999] == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert results[10651060] == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790,
                           1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == '__main__':
    main((128, 255, 99999, 10651060))
