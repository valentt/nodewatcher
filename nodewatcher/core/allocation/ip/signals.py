from django import dispatch

# Called by IpAddressAllocatorFormMixin to further filter the pools, which are
# contained in pool.queryset where pool is the underlying form field.
filter_pools = dispatch.Signal()
