# 囫囵吞枣不插电源码-类加载
## 核心cpp
classfile/classFileParser.hpp 解析，校验，初始化
classfile/classFileStream.hpp 就是stream及简单校验
classfile/classLoader.hpp 类加载总类
classfile/systemDictionary.hpp 类加载完元信息放到这里
classfile/vmSymbols.hpp 一些乱七八糟的信息
## ClassLoader
```
instanceKlassHandle ClassLoader::load_classfile(Symbol* h_name, TRAPS) {
  ResourceMark rm(THREAD);
  EventMark m("loading class " INTPTR_FORMAT, (address)h_name);
  ThreadProfilerMark tpm(ThreadProfilerMark::classLoaderRegion);

  stringStream st;
  // st.print() uses too much stack space while handling a StackOverflowError
  // st.print("%s.class", h_name->as_utf8());
  st.print_raw(h_name->as_utf8());
  st.print_raw(".class");
  char* name = st.as_string();

  // Lookup stream for parsing .class file
  ClassFileStream* stream = NULL;
  int classpath_index = 0;
  {
    PerfClassTraceTime vmtimer(perf_sys_class_lookup_time(),
                               ((JavaThread*) THREAD)->get_thread_stat()->perf_timers_addr(),
                               PerfClassTraceTime::CLASS_LOAD);
    ClassPathEntry* e = _first_entry;
    while (e != NULL) {
      stream = e->open_stream(name);
      if (stream != NULL) {
        break;
      }
      e = e->next();
      ++classpath_index;
    }
  }
```
* ResourceMark
ResourceMark->StackObj->AllocatedObj
用来初始化申请栈和堆资源
   1. ResourceArea->Arena->CHeapObj<mtNone|otArena>->AllocatedObj
       1. A ResourceArea is an Arena that supports safe usage of ResourceMark.
       2.  Resource area to stack allocate
   2. Chunk->CHeapObj->AllocatedObj
       1. saved arena chunk
* EventMark
打印日志用的，加入一个list 排队打印
EventMark->StackObj->AllocatedObj
* ThreadProfilerMark
获取region标记
ThreadProfilerMark->StackObj->AllocatedObj
* 打印
* PerfClassTraceTime vmtimer 初始化为 CLASS_LOAD
```
    CLASS_LOAD   = 0,
    PARSE_CLASS  = 1,
    CLASS_LINK   = 2,
    CLASS_VERIFY = 3,
    CLASS_CLINIT = 4,
    DEFINE_CLASS = 5,
    EVENT_TYPE_COUNT = 6
```
* instanceKlassHandle
    * ClassFileParser
       ```
       private:
        bool _need_verify;
        bool _relax_verify;
        u2   _major_version;
        u2   _minor_version;
        Symbol* _class_name;
        ClassLoaderData* _loader_data;
        KlassHandle _host_klass;
        GrowableArray<Handle>* _cp_patches; // overrides for CP entries

        // precomputed flags
        bool _has_finalizer;
        bool _has_empty_finalizer;
        bool _has_vanilla_constructor;
        int _max_bootstrap_specifier_index;  // detects BSS values

        // class attributes parsed before the instance klass is created:
        bool       _synthetic_flag;
        int        _sde_length;
        char*      _sde_buffer;
        Symbol*    _sourcefile;
        Symbol*    _generic_signature;

        // Metadata created before the instance klass is created.  Must be deallocated
        // if not transferred to the InstanceKlass upon successful class loading
        // in which case these pointers have been set to NULL.
        instanceKlassHandle _super_klass;
        ConstantPool*    _cp;
        Array<u2>*       _fields;
        Array<Method*>*  _methods;
        Array<u2>*       _inner_classes;
        Array<Klass*>*   _local_interfaces;
        Array<Klass*>*   _transitive_interfaces;
        AnnotationArray* _annotations;
        AnnotationArray* _type_annotations;
        Array<AnnotationArray*>* _fields_annotations;
        Array<AnnotationArray*>* _fields_type_annotations;
        InstanceKlass*   _klass;  // InstanceKlass once created.
       ```       
       ```
        instanceKlassHandle ClassFileParser::parseClassFile(Symbol* name,
                                                    ClassLoaderData* loader_data,
                                                    Handle protection_domain,
                                                    KlassHandle host_klass,
                                                    GrowableArray<Handle>* cp_patches,
                                                    TempNewSymbol& parsed_name,
                                                    bool verify,
                                                    TRAPS) {

        // When a retransformable agent is attached, JVMTI caches the
        // class bytes that existed before the first retransformation.
        // If RedefineClasses() was used before the retransformable
        // agent attached, then the cached class bytes may not be the
        // original class bytes.
        unsigned char *cached_class_file_bytes = NULL;
        jint cached_class_file_length;
        Handle class_loader(THREAD, loader_data->class_loader());
        bool has_default_methods = false;
        ResourceMark rm(THREAD);

        ClassFileStream* cfs = stream();
        // Timing
        assert(THREAD->is_Java_thread(), "must be a JavaThread");
        JavaThread* jt = (JavaThread*) THREAD;

        PerfClassTraceTime ctimer(ClassLoader::perf_class_parse_time(),
                                    ClassLoader::perf_class_parse_selftime(),
                                    NULL,
                                    jt->get_thread_stat()->perf_recursion_counts_addr(),
                                    jt->get_thread_stat()->perf_timers_addr(),
                                    PerfClassTraceTime::PARSE_CLASS);

        init_parsed_class_attributes(loader_data);

        if (JvmtiExport::should_post_class_file_load_hook()) {
            // Get the cached class file bytes (if any) from the class that
            // is being redefined or retransformed. We use jvmti_thread_state()
            // instead of JvmtiThreadState::state_for(jt) so we don't allocate
            // a JvmtiThreadState any earlier than necessary. This will help
            // avoid the bug described by 7126851.
            JvmtiThreadState *state = jt->jvmti_thread_state();
            if (state != NULL) {
            KlassHandle *h_class_being_redefined =
                            state->get_class_being_redefined();
            if (h_class_being_redefined != NULL) {
                instanceKlassHandle ikh_class_being_redefined =
                instanceKlassHandle(THREAD, (*h_class_being_redefined)());
                cached_class_file_bytes =
                ikh_class_being_redefined->get_cached_class_file_bytes();
                cached_class_file_length =
                ikh_class_being_redefined->get_cached_class_file_len();
            }
            }

            unsigned char* ptr = cfs->buffer();
            unsigned char* end_ptr = cfs->buffer() + cfs->length();

            JvmtiExport::post_class_file_load_hook(name, class_loader(), protection_domain,
                                                &ptr, &end_ptr,
                                                &cached_class_file_bytes,
                                                &cached_class_file_length);

            if (ptr != cfs->buffer()) {
            // JVMTI agent has modified class file data.
            // Set new class file stream using JVMTI agent modified
            // class file data.
            cfs = new ClassFileStream(ptr, end_ptr - ptr, cfs->source());
            set_stream(cfs);
            }
        }
       ```
       parseClassFile流程:
       1. 各种初始化声明：cached_class_file_bytes，has_default_methods,class_loader,ResourceMark,ClassFileStream,JavaThread,PerfClassTraceTime::PARSE_CLASS
       2. init_parsed_class_attributes: 初始化元数据信息
        ```
            void init_parsed_class_attributes(ClassLoaderData* loader_data) {
            _loader_data = loader_data;
            _synthetic_flag = false;
            _sourcefile = NULL;
            _generic_signature = NULL;
            _sde_buffer = NULL;
            _sde_length = 0;
            // initialize the other flags too:
            _has_finalizer = _has_empty_finalizer = _has_vanilla_constructor = false;
            _max_bootstrap_specifier_index = -1;
            clear_class_metadata();
            _klass = NULL;
        }
        void clear_class_metadata() {
            // metadata created before the instance klass is created.  Must be
            // deallocated if classfile parsing returns an error.
            _cp = NULL;
            _fields = NULL;
            _methods = NULL;
            _inner_classes = NULL;
            _local_interfaces = NULL;
            _transitive_interfaces = NULL;
            _annotations = _type_annotations = NULL;
            _fields_annotations = _fields_type_annotations = NULL;
        }
        ```
       3. 判断是否hook should_post_class_file_load_hook
            有的话设置cached_class_file_bytes= redefined.getcache
       4. JVMTI设置 JvmtiExport::post_class_file_load_hook->JvmtiClassFileLoadHookPoster poster.post()
          更新hook，如果有变更则重新创建ClassFileStream()
       5. 设置kclassHanle(host_klass),设置GrowableArray<Handle>（cp_patches）调用链，instanceKlassHandle（nullHandle），设置是否需要校验，设置class_name
       6. 校验magic(u4), major(u2), minor(u2)->java_lang_UnsupportedClassVersionError，松弛校验
       7.  ConstantPoolHandle设置， flags(u2), this_class(u2), super_class, infs_len校验
       8.  Interfaces(u2),Fields(u2),Methods,Additional attributes,eof
       9.  检查superclass 没有就加载，并确认验证是否有默认方法，是否接口，是否final，统计接口实现信息，method sort
       10. compute_vtable_size_and_num_mirandas：vtable和米兰达方法，itable统计，Compute reference type
       11. allocate_instance_klass//实例化对象
    ```
             _klass = InstanceKlass::allocate_instance_klass(loader_data,
                                                    vtable_size,
                                                    itable_size,
                                                    info.static_field_size,
                                                    total_oop_map_size2,
                                                    rt,
                                                    access_flags,
                                                    name,
                                                    super_klass(),
                                                    !host_klass.is_null(),
                                                    CHECK_(nullHandle));
            this_klass->set_should_verify_class(verify);
            jint lh = Klass::instance_layout_helper(info.instance_size, false);
            this_klass->set_layout_helper(lh);
            assert(this_klass->oop_is_instance(), "layout is correct");
            assert(this_klass->size_helper() == info.instance_size, "correct size_helper");
            // Not yet: supers are done below to support the new subtype-checking fields
            //this_klass->set_super(super_klass());
            this_klass->set_class_loader_data(loader_data);
            this_klass->set_nonstatic_field_size(info.nonstatic_field_size);
            this_klass->set_has_nonstatic_fields(info.has_nonstatic_fields);
            this_klass->set_static_oop_field_count(fac.count[STATIC_OOP]);

            apply_parsed_class_metadata(this_klass, java_fields_count, CHECK_NULL);

            if (has_final_method) {
            this_klass->set_has_final_method();
            }
            this_klass->copy_method_ordering(method_ordering, CHECK_NULL);
            // The InstanceKlass::_methods_jmethod_ids cache and the
            // InstanceKlass::_methods_cached_itable_indices cache are
            // both managed on the assumption that the initial cache
            // size is equal to the number of methods in the class. If
            // that changes, then InstanceKlass::idnum_can_increment()
            // has to be changed accordingly.
            this_klass->set_initial_method_idnum(methods->length());
            this_klass->set_name(cp->klass_name_at(this_class_index));
            if (is_anonymous())  // I am well known to myself
            cp->klass_at_put(this_class_index, this_klass()); // eagerly resolve

            this_klass->set_minor_version(minor_version);
            this_klass->set_major_version(major_version);
            this_klass->set_has_default_methods(has_default_methods);

            // Set up Method*::intrinsic_id as soon as we know the names of methods.
            // (We used to do this lazily, but now we query it in Rewriter,
            // which is eagerly done for every method, so we might as well do it now,
            // when everything is fresh in memory.)
            if (Method::klass_id_for_intrinsics(this_klass()) != vmSymbols::NO_SID) {
            for (int j = 0; j < methods->length(); j++) {
                methods->at(j)->init_intrinsic_id();
            }
            }

            if (cached_class_file_bytes != NULL) {
            // JVMTI: we have an InstanceKlass now, tell it about the cached bytes
            this_klass->set_cached_class_file(cached_class_file_bytes,
                                                cached_class_file_length);
            }

            // Fill in field values obtained by parse_classfile_attributes
            if (parsed_annotations.has_any_annotations())
            parsed_annotations.apply_to(this_klass);
            apply_parsed_class_attributes(this_klass);

            // Miranda methods
            if ((num_miranda_methods > 0) ||
                // if this class introduced new miranda methods or
                (super_klass.not_null() && (super_klass->has_miranda_methods()))
                // super class exists and this class inherited miranda methods
                ) {
            this_klass->set_has_miranda_methods(); // then set a flag
            }

            // Fill in information needed to compute superclasses.
            this_klass->initialize_supers(super_klass(), CHECK_(nullHandle));

            // Initialize itable offset tables
            klassItable::setup_itable_offset_table(this_klass);
            // Compute transitive closure of interfaces this class implements
            // Do final class setup
            fill_oop_maps(this_klass, info.nonstatic_oop_map_count, info.nonstatic_oop_offsets, info.nonstatic_oop_counts);

            // Fill in has_finalizer, has_vanilla_constructor, and layout_helper
            set_precomputed_flags(this_klass);

            // reinitialize modifiers, using the InnerClasses attribute
            int computed_modifiers = this_klass->compute_modifier_flags(CHECK_(nullHandle));
            this_klass->set_modifier_flags(computed_modifiers);

            // check if this class can access its super class
            check_super_class_access(this_klass, CHECK_(nullHandle));

            // check if this class can access its superinterfaces
            check_super_interface_access(this_klass, CHECK_(nullHandle));

            // check if this class overrides any final method
            check_final_method_override(this_klass, CHECK_(nullHandle));

            // check that if this class is an interface then it doesn't have static methods
            if (this_klass->is_interface()) {
            /* An interface in a JAVA 8 classfile can be static */
            if (_major_version < JAVA_8_VERSION) {
                check_illegal_static_method(this_klass, CHECK_(nullHandle));
            }
            }

            // Allocate mirror and initialize static fields
            java_lang_Class::create_mirror(this_klass, protection_domain, CHECK_(nullHandle));
            // Generate any default methods - default methods are interface methods
            // that have a default implementation.  This is new with Lambda project.
            if (has_default_methods && !access_flags.is_interface() &&
                local_interfaces->length() > 0) {
            DefaultMethods::generate_default_methods(
                this_klass(), &all_mirandas, CHECK_(nullHandle));
            }

            // Update the loader_data graph.
            record_defined_class_dependencies(this_klass, CHECK_NULL);
            ClassLoadingService::notify_class_loaded(InstanceKlass::cast(this_klass()),
                                                    false /* not shared class */);
                if (TraceClassLoading) {
                ResourceMark rm;
                // print in a single call to reduce interleaving of output
                if (cfs->source() != NULL) {
                    tty->print("[Loaded %s from %s]\n", this_klass->external_name(),
                            cfs->source());
                } else if (class_loader.is_null()) {
                    if (THREAD->is_Java_thread()) {
                    Klass* caller = ((JavaThread*)THREAD)->security_get_caller_class(1);
                    tty->print("[Loaded %s by instance of %s]\n",
                                this_klass->external_name(),
                                InstanceKlass::cast(caller)->external_name());
                    } else {
                    tty->print("[Loaded %s]\n", this_klass->external_name());
                    }
                } else {
                    tty->print("[Loaded %s from %s]\n", this_klass->external_name(),
                            InstanceKlass::cast(class_loader->klass())->external_name());
                }
                }

            if (TraceClassResolution) {
            ResourceMark rm;
            // print out the superclass.
            const char * from = this_klass()->external_name();
            if (this_klass->java_super() != NULL) {
                tty->print("RESOLVE %s %s (super)\n", from, InstanceKlass::cast(this_klass->java_super())->external_name());
            }
            // print out each of the interface classes referred to by this class.
            Array<Klass*>* local_interfaces = this_klass->local_interfaces();
            if (local_interfaces != NULL) {
                int length = local_interfaces->length();
                for (int i = 0; i < length; i++) {
                Klass* k = local_interfaces->at(i);
                InstanceKlass* to_class = InstanceKlass::cast(k);
                const char * to = to_class->external_name();
                tty->print("RESOLVE %s %s (interface)\n", from, to);
                }
            }
            }

            // preserve result across HandleMark
            preserve_this_klass = this_klass();
            }

            // Create new handle outside HandleMark (might be needed for
            // Extended Class Redefinition)
            instanceKlassHandle this_klass (THREAD, preserve_this_klass);
            debug_only(this_klass->verify();)

            // Clear class if no error has occurred so destructor doesn't deallocate it
            _klass = NULL;
            return this_klass;
    ```
    InstanceKlass的操作
    ```            
            InstanceKlass* InstanceKlass::allocate_instance_klass(
                                                ClassLoaderData* loader_data,
                                                int vtable_len,
                                                int itable_len,
                                                int static_field_size,
                                                int nonstatic_oop_map_size,
                                                ReferenceType rt,
                                                AccessFlags access_flags,
                                                Symbol* name,
                                                Klass* super_klass,
                                                bool is_anonymous,
                                                TRAPS) {

            int size = InstanceKlass::size(vtable_len, itable_len, nonstatic_oop_map_size,
                                            access_flags.is_interface(), is_anonymous);

            // Allocation
            InstanceKlass* ik;
            if (rt == REF_NONE) {
                if (name == vmSymbols::java_lang_Class()) {
                ik = new (loader_data, size, THREAD) InstanceMirrorKlass(
                    vtable_len, itable_len, static_field_size, nonstatic_oop_map_size, rt,
                    access_flags, is_anonymous);
                } else if (name == vmSymbols::java_lang_ClassLoader() ||
                    (SystemDictionary::ClassLoader_klass_loaded() &&
                    super_klass != NULL &&
                    super_klass->is_subtype_of(SystemDictionary::ClassLoader_klass()))) {
                ik = new (loader_data, size, THREAD) InstanceClassLoaderKlass(
                    vtable_len, itable_len, static_field_size, nonstatic_oop_map_size, rt,
                    access_flags, is_anonymous);
                } else {
                // normal class
                ik = new (loader_data, size, THREAD) InstanceKlass(
                    vtable_len, itable_len, static_field_size, nonstatic_oop_map_size, rt,
                    access_flags, is_anonymous);
                }
            } else {
                // reference klass
                ik = new (loader_data, size, THREAD) InstanceRefKlass(
                    vtable_len, itable_len, static_field_size, nonstatic_oop_map_size, rt,
                    access_flags, is_anonymous);
            }

            // Check for pending exception before adding to the loader data and incrementing
            // class count.  Can get OOM here.
            if (HAS_PENDING_EXCEPTION) {
                return NULL;
            }

            // Add all classes to our internal class loader list here,
            // including classes in the bootstrap (NULL) class loader.
            loader_data->add_class(ik);

            Atomic::inc(&_total_instanceKlass_count);
            return ik;
            }
    ```
       
    * add_package
    * initialize
    * UsePerfData?->jvmstat performance counters
    * load_zip_library
    * setup_bootstrap_search_path
    * LazyBootClassLoader?->setup_meta_index

## 引用
https://hllvm-group.iteye.com/group/topic/35385#post-236056