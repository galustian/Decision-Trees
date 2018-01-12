class Tree():
    def __init__(self, max_depth=6, min_size=5):
        self.max_depth = max_depth
        self.min_size = min_size


    def fit(self, df_train):
        root = self.__get_best_split(df_train)
        self.__split(root, se 1)
        self.root = root


    def predict(self, row):
        return self.__predict(self.root, row)
       

    @staticmethod
    def __predict(node, row):
         if row[node['index']] < node['value']:
            if isinstance(node['left'], dict):
                return predict(node['left'], row)
            else:
                return node['left']
        else:
            if isinstance(node['right'], dict):
                return predict(node['right'], row)
            else:
                return node['right']


    def print_tree(self):
        self.__print_tree(self.root, 0)
    
    @staticmethod
    def __print_tree(node, depth)
        if isinstance(node, dict):
            print("{}[{} < {}]".format(depth*' ', node['index'], node['value']))
            print_tree(node['left'], depth+1)
            print_tree(node['right'], depth+1)
        else:
            print("{}, => {}".format(depth*' ', node))


    @staticmethod
    def __gini_index(bi_split, classes):
        # count all samples in both data-splits
        n_datapoints = float(sum([len(g) for g in bi_split]))

        # calculate and sum gini for both groups
        gini = 0.0
        for group in bi_split:
            size = float(len(group))
            if size == 0:
                continue

            score = 0.0
            classes_amount = group.iloc[:, -1].value_counts()
            for class_val in classes:
                if len(classes_amount) == 1: continue
                prop = classes_amount[class_val] / size
                score += prop * (1 - prop)

            # weight the group score by its relative size
            gini += score * (size / n_datapoints)

        return gini


    @staticmethod
    def __test_split(index, value, df):
        left_split = df[df[index] < value]
        right_split = df[df[index] >= value]
        return left_split, right_split


    # creates node with bi_split data
    def __get_best_split(self, df):
        class_values = df.iloc[:, -1].unique()
        b_index, b_value, b_score, b_split= 9999, 9999, 9999, None
        
        for index in range(df.shape[1]-1):
            for i, row in df.iterrows():
                # don't check gini_index for every split-size (too expensive)
                # instead for every min_size'th row
                if i % self.min_size != 0: continue

                bi_split = self.__test_split(index, row[index], df)
                gini = self.__gini_index(bi_split, class_values)
                if gini < b_score:
                    b_index, b_value, b_score, b_split = index, row[index], gini, bi_split
        
        return {'index': b_index, 'value': b_value, 'bi_split': b_split}



    @staticmethod
    def __to_terminal(df_group):
        return df_group.iloc[:, -1].value_counts().idxmax()



    def __split(self, node, depth):
        left, right = node['bi_split']
        del(node['bi_split'])
        
        # if either left or right df have length 0, then they are both the same class
        # => you can't split them anymore => create terminal-node
        if len(left) == 0 or len(right) == 0:
            node['left'] = node['right'] = self.__to_terminal(left.append(right))
            return
            
        # check for max depth
        if depth >= self.max_depth:
            node['left'], node['right'] = self.__to_terminal(left), self.__to_terminal(right)
            return
        
        # process left child
        if len(left) <= self.min_size:
            node['left'] = self.__to_terminal(left)
        else:
            node['left'] = self.__get_best_split(left)
            self.__split(self, node['left'], depth+1)
        
        # process right child
        if len(right) <= self.min_size:
            node['right'] = self.__to_terminal(right)
        else:
            node['right'] = self.__get_best_split(right)
            self.__split(self, node['right'], depth+1)