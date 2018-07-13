import unittest
from collections import Counter

import numpy as np

from dataset.utils import balance_data, extract_label2imgs, train_test_split, shuffle

######################################################################
#  T E S T   C A S E S
######################################################################
class TestDataset(unittest.TestCase):
    """ Test Cases for dataset """

    def test_shuffle(self):
        """ Test shuffle """
        images = [1,2,3]
        labels = [4,5,6]
        img2label = {1:4, 2:5, 3:6}

        # just test shuffle, so no duplicate image in images are allowed
        data = {'images': np.array(images), 'labels': np.array(labels)}
        test_times = 3

        for _ in range(test_times):
            shuffled_data = shuffle(data)

            self.assertIsNot(data, shuffled_data)
            self.assertEqual(shuffled_data['images'].shape[0], data['images'].shape[0])
            self.assertEqual(shuffled_data['labels'].shape[0], data['labels'].shape[0])

            for key in img2label.keys():
                self.assertIn(key, shuffled_data['images'])
                index = np.where(shuffled_data['images'] == key)[0][0]
                val = shuffled_data['labels'][index]
                self.assertEqual(img2label[key], val)

    def test_extract_label2imgs(self):
        """ Test extract_label2imgs """
        images = [1,2,3]
        labels = [4,4,6]
        all_labels = [4,6]
        self_label2imgs = {4:[1,2], 6:[3]}
        
        data = {'images': np.array(images), 'labels': np.array(labels)}

        label2imgs = extract_label2imgs(data, all_labels)
        self.assertEqual(set(self_label2imgs.keys()), set(labels))
        self.assertEqual(set(label2imgs.keys()), set(labels))
        for label in set(labels):
            label2imgs[label].sort()
            self_label2imgs[label].sort()
            self.assertTrue((self_label2imgs[label] == label2imgs[label]).all())
        
        all_labels = [4,5]
        with self.assertRaises(AssertionError):
            extract_label2imgs(data, all_labels)
        
        all_labels = [4,6,5]
        with self.assertRaises(AssertionError):
            extract_label2imgs(data, all_labels)
        
        all_labels = [4]
        with self.assertRaises(AssertionError):
            extract_label2imgs(data, all_labels)
    
    def test_balance_data(self):
        """ Test balance_data """
        images = [1,2,3,5]
        labels = [4,4,6,0]
        self_res_labels = [6,4,0]
        all_labels = [4,6,0]
        data = {'images': np.array(images), 'labels': np.array(labels)}
        img2label = {1:4,2:4,3:6,5:0}
        test_times = 3

        for _ in range(test_times):
            balanced_data = balance_data(data, all_labels)
            self.assertEqual(set(balanced_data['labels']), set(labels))
            self.assertEqual(Counter(balanced_data['labels']), Counter(self_res_labels))
            for img, label in zip(balanced_data['images'], balanced_data['labels']):
                self.assertEqual(img2label[img], label)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()