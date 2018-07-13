import unittest
from collections import Counter
from copy import deepcopy

import numpy as np

from dataset.utils import balance_data, extract_label2imgs, train_test_split, shuffle

#TODO: should be tested, too
# recommendation: move to utils module
def list_contained_in(l1, l2):
    """
    Checks whether l1 is contained in l2. Will not affect the original value order in l1 and l2
    """
    sorted_l1 = sorted(l1)
    sorted_l2 = sorted(l2)
    l2_iter = iter(sorted_l2)
    return all(item in l2_iter for item in sorted_l1)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestDataset(unittest.TestCase):
    """ Test Cases for dataset """

    #TODO: should use 2d images
    def test_shuffle(self):
        """ Test shuffle """
        images = [[1],[2],[3]]
        labels = [4,4,6]
        label2imgs = {4:[[1],[2]], 6:[[3]]}

        data = {'images': np.array(images), 'labels': np.array(labels)}
        test_times = 3

        for _ in range(test_times):
            copied_label2imgs = deepcopy(label2imgs)
            shuffled_data = shuffle(data)

            # test instance equality
            self.assertIsNot(data, shuffled_data)

            # test shape
            self.assertEqual(shuffled_data['images'].shape, data['images'].shape)
            self.assertEqual(shuffled_data['labels'].shape, data['labels'].shape)

            # test one-to-one mapping
            for img, label in zip(shuffled_data['images'], shuffled_data['labels']):
               self.assertIn(img, copied_label2imgs[label])
               copied_label2imgs[label].remove(img)
            self.assertTrue(all(val == [] for val in copied_label2imgs.values()))

    def test_extract_label2imgs(self):
        """ Test extract_label2imgs """
        images = [[1],[2],[3]]
        labels = [4,4,6]
        all_labels = list(set(labels))
        self_label2imgs = {4:[[1],[2]], 6:[[3]]}
        
        data = {'images': np.array(images), 'labels': np.array(labels)}

        label2imgs = extract_label2imgs(data, all_labels)
        self.assertEqual(set(self_label2imgs.keys()), set(labels))
        self.assertEqual(set(label2imgs.keys()), set(labels))
        for label in set(labels):
            self.assertTrue(sorted(self_label2imgs[label]) == sorted(label2imgs[label]))
        
        all_labels = [4,5]
        with self.assertRaises(AssertionError):
            extract_label2imgs(data, all_labels)
        
        all_labels = [4,6,5]
        with self.assertRaises(AssertionError):
            extract_label2imgs(data, all_labels)
        
        all_labels = [4]
        with self.assertRaises(AssertionError):
            extract_label2imgs(data, all_labels)
    
    #TODO: should use 2d images
    def test_balance_data(self):
        """ Test balance_data """
        images = [1,2,3,5]
        labels = [4,4,6,0]
        self_res_labels = [6,4,0]
        all_labels = list(set(labels))
        data = {'images': np.array(images), 'labels': np.array(labels)}
        img2label = dict(zip(images,labels))
        test_times = 3

        for _ in range(test_times):
            balanced_data = balance_data(data, all_labels)

            self.assertEqual(balanced_data['images'].shape[0], balanced_data['labels'].shape[0])

            self.assertEqual(set(balanced_data['labels']), set(labels))
            self.assertEqual(Counter(balanced_data['labels']), Counter(self_res_labels))
            self.assertTrue(list_contained_in(balanced_data['images'], images))
            self.assertTrue(list_contained_in(balanced_data['labels'], labels))
            for img, label in zip(balanced_data['images'], balanced_data['labels']):
                self.assertEqual(img2label[img], label)
    
    #TODO: should use 2d images
    def test_train_test_split(self):
        """ Test train_test_split """
        # normal occasions
        images = [1,2,3,4,5,6,7]
        labels = [4,4,6,6,0,0,0]
        all_labels = list(set(labels))

        data = {'images': np.array(images), 'labels': np.array(labels)}
        img2label = dict(zip(images,labels))
        test_times = 3
        train_ratio = 0.5
        
        for _ in range(test_times):
            train, test = train_test_split(data, all_labels, train_ratio)

            self.assertEqual(train['images'].shape[0], train['labels'].shape[0])
            self.assertEqual(test['images'].shape[0], test['labels'].shape[0])

            self.assertEqual(train['labels'].shape[0], int(len(labels) * train_ratio))
            self.assertEqual(test['labels'].shape[0], len(labels) - int(len(labels) * train_ratio))

            res_images = np.append(train['images'], test['images'])
            res_labels = np.append(train['labels'], test['labels'])
            self.assertTrue(list_contained_in(res_images, images))
            self.assertTrue(list_contained_in(res_labels, labels))

            label_counter = Counter(train['labels'])
            most_common_labels = label_counter.most_common()
            self.assertTrue(most_common_labels[0][1] - most_common_labels[-1][1] <= 1)

            for img, label in zip(res_images, res_labels):
                self.assertEqual(img2label[img], label)
        
        # abnormal occasions
        # 1
        images = [1,2,3,4,5,6,7]
        labels = [4,4,3,2,4,6,2]

        all_labels = list(set(labels))
        data = {'images': np.array(images), 'labels': np.array(labels)}
        img2label = dict(zip(images,labels))
        test_times = 3
        train_ratio = 0.5
        with self.assertRaises(AssertionError):
            train_test_split(data, all_labels, train_ratio)

        # 2
        images = [1,2,3,4,5,6,7]
        labels = [0,4,4,4,4,4,4]

        all_labels = list(set(labels))
        data = {'images': np.array(images), 'labels': np.array(labels)}
        img2label = dict(zip(images,labels))
        test_times = 3
        train_ratio = 0.5
        with self.assertRaises(AssertionError):
            train_test_split(data, all_labels, train_ratio)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()