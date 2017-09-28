from __future__ import print_function
import tensorflow as tf
from layers.conv_layers import multiLayer_conv_strip
from app.params import convRankParams 
from models.base_model import regressModel
from layers.common_layers import semantic_position_embedding
from pydoc import locate

class convRank(regressModel):
            def _forward_(self):
                        # input coding placeholder
                        self.source = tf.placeholder(shape=(None, convRankParams.source_maxlen),dtype=tf.int64)
                        self.tag = tf.placeholder(shape=(None, ),dtype=tf.int64)
                        self.target = tf.placeholder(shape=(None, ),dtype=tf.float32)

                        encoding = semantic_position_embedding(
                                                            inputs=self.source,
                                                            vocab_size=convRankParams.source_vocab_size,
                                                            num_units=convRankParams.embedding_dim,
                                                            maxlen=convRankParams.source_maxlen,
                                                            scope='encoder')

                        encoding = multiLayer_conv_strip(
                                                      inputs=encoding,
                                                      is_training=self.is_training,
                                                      is_dropout=self.is_dropout)

                        conv_c_out = tf.layers.dense(
                                                inputs=encoding,
                                                units=convRankParams.hidden_units,
                                                name="conv_full",
                                                activation=locate(convRankParams.activation_fn))

                        tagEmbed = embedding(
                                          inputs=self.tag,
                                          vocab_size=convRankParams.tag_size,
                                          num_units=convRankParams.embedding_dim,
                                          zero_pad=False,
                                          scale=True,
                                          scope="tagEmbed")

                        full_layer = tf.concat([tagEmbed,conv_c_out],1)

                        self.logits = mlp_layer(
                                                inputs=full_layer,
                                                output_dim=1,
                                                mlp_layers=convRankParams.mlp_layers,
                                                activation_fn=locate(convRankParams.activation_fn),
                                                is_training=self.is_training,
                                                is_dropout=self.is_dropout)
                        # saver
                        self.global_saver = tf.train.Saver()