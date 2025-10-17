app:
  description: Google Keyword Planner APIを使用してSEOキーワード戦略を提案するAI社員
  icon: 🔍
  icon_background: '#10B981'
  mode: workflow
  name: SEOキーワード設計AI
  use_icon_as_answer_icon: false

version: 0.4.0
kind: app

workflow:
  conversation_variables: []
  environment_variables:
  - variable: GOOGLE_API_KEY
    name: Google Keyword Planner APIキー
    value: your_api_key_here
  - variable: GOOGLE_API_URL
    name: Keyword Planner API URL
    value: https://googleads.googleapis.com/google.ads.googleads.v16/customers/YOUR_CUSTOMER_ID/keywords
  features:
    file_upload:
      enabled: true
      allowed_file_extensions:
      - .txt
      - .csv
      - .md
      allowed_file_types:
      - document
      allowed_file_upload_methods:
      - local_file
      - remote_url
      fileUploadConfig:
        file_size_limit: 50
        batch_count_limit: 10
        workflow_file_upload_limit: 10
      image:
        enabled: false
      number_limits: 10
    opening_statement: ターゲットキーワード、ビジネス情報、競合URLを入力して、最適なSEOキーワード戦略を取得します。
    retriever_resource:
      enabled: false
    sensitive_word_avoidance:
      enabled: false
    speech_to_text:
      enabled: false
    suggested_questions:
    - Eコマース向けのキーワード戦略を提案してください
    - 地域ビジネスのローカルSEO対策を教えてください
    suggested_questions_after_answer:
      enabled: false
    text_to_speech:
      enabled: false
      language: ''
      voice: ''
  graph:
    nodes:
    - data:
        desc: SEOキーワード分析の入力情報
        selected: true
        title: 開始
        type: start
        variables:
        - label: ターゲットキーワード
          variable: target_keyword
          type: text-input
          max_length: 500
          required: true
          options: []
        - label: ビジネス情報（業種・サービス内容）
          variable: business_info
          type: paragraph
          max_length: 2000
          required: true
          options: []
        - label: 競合URL（テキスト形式）
          variable: competitor_urls_text
          type: paragraph
          max_length: 1000
          required: false
          options: []
        - label: 競合情報ファイル（複数選択可）
          variable: competitor_files
          type: file-list
          required: false
          options: []
        - label: 分析タイプ
          variable: analysis_type
          type: select
          required: true
          options:
          - value: standard
            label: 標準分析（キーワードボリューム・難易度）
          - value: comprehensive
            label: 包括分析（トレンド・意図分析含む）
          - value: competitive
            label: 競合分析重視
      height: 240
      id: start
      position:
        x: 80
        y: 200
      positionAbsolute:
        x: 80
        y: 200
      selected: true
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        title: 入力形式の判定
        type: if-else
        cases:
        - case_id: 'text_only'
          conditions:
          - variable_selector:
            - start
            - competitor_urls_text
            operator: 'is-not-empty'
          id: 'text_only'
          logical_operator: and
        - case_id: 'files_only'
          conditions:
          - variable_selector:
            - start
            - competitor_files
            operator: 'is-not-empty'
          id: 'files_only'
          logical_operator: and
        - case_id: 'both'
          conditions:
          - variable_selector:
            - start
            - competitor_urls_text
            operator: 'is-not-empty'
          - variable_selector:
            - start
            - competitor_files
            operator: 'is-not-empty'
          id: 'both'
          logical_operator: and
        desc: テキスト入力とファイル入力を判定
        selected: false
      height: 150
      id: input_condition
      position:
        x: 400
        y: 200
      positionAbsolute:
        x: 400
        y: 200
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        title: ファイル処理ループ
        type: loop
        loop_count: 10
        start_node_id: file_loop_start
        desc: 複数のファイルを処理
        selected: false
      height: 195
      id: file_loop
      position:
        x: 720
        y: 50
      positionAbsolute:
        x: 720
        y: 50
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 400
      zIndex: 1
    - data:
        desc: ''
        isInLoop: true
        selected: false
        title: ''
        type: loop-start
      draggable: false
      height: 48
      id: file_loop_start
      parentId: file_loop
      position:
        x: 24
        y: 68
      positionAbsolute:
        x: 744
        y: 118
      selectable: false
      sourcePosition: right
      targetPosition: left
      type: custom-loop-start
      width: 44
      zIndex: 1002
    - data:
        desc: ファイル内容を抽出
        isInLoop: true
        selected: false
        template: '{{ file_content }}'
        title: ファイル内容抽出
        type: template-transform
        variables:
        - value_selector: []
          variable: file_content
      height: 53
      id: file_extract
      position:
        x: 128
        y: 68
      positionAbsolute:
        x: 752
        y: 118
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
      zIndex: 1002
    - data:
        context:
          enabled: false
          variable_selector: []
        desc: Google Keyword Planner APIにキーワード情報をリクエスト
        model:
          completion_params:
            temperature: 0
            max_tokens: 500
          mode: chat
          name: claude-opus-4-1-20250805
          provider: langgenius/anthropic/anthropic
        prompt_template:
        - id: api_request_builder
          role: user
          text: |
            以下のキーワードについてGoogle Keyword Planner APIにリクエストするためのJSON形式を作成してください：
            
            キーワード: {{#start.target_keyword#}}
            ビジネス情報: {{#start.business_info#}}
            分析タイプ: {{#start.analysis_type#}}
            
            JSONフォーマット:
            {
              "keywords": ["キーワード"],
              "businessInfo": "ビジネス情報",
              "analysisType": "standard|comprehensive|competitive"
            }
        selected: false
        title: APIリクエスト生成
        type: llm
        variables: []
        vision:
          enabled: false
      height: 90
      id: api_builder_llm
      position:
        x: 720
        y: 300
      positionAbsolute:
        x: 720
        y: 300
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        authorization:
          config: null
          type: bearer-token
        body:
          data:
          - key: requestBody
            type: text
            value: '{{#api_builder_llm.text#}}'
        desc: Google Keyword Planner APIへリクエスト送信
        headers: 'Authorization: Bearer {{#env.GOOGLE_API_KEY#}}'
        method: POST
        params: ''
        retry_config:
          max_retries: 3
          retry_enabled: true
          retry_interval: 1000
        selected: false
        ssl_verify: true
        timeout:
          max_connect_timeout: 10000
          max_read_timeout: 30000
          max_write_timeout: 10000
        title: Google Keyword Planner API呼び出し
        type: http-request
        url: '{{#env.GOOGLE_API_URL#}}'
        variables: []
      height: 90
      id: google_api_request
      position:
        x: 1040
        y: 300
      positionAbsolute:
        x: 1040
        y: 300
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        context:
          enabled: false
          variable_selector: []
        desc: APIレスポンスを分析してキーワード戦略を提案
        model:
          completion_params:
            temperature: 0.7
            max_tokens: 1500
          mode: chat
          name: claude-opus-4-1-20250805
          provider: langgenius/anthropic/anthropic
        prompt_template:
        - id: keyword_analysis_prompt
          role: user
          text: |
            Google Keyword Planner APIの結果を分析して、キーワード戦略を提案してください。
            
            【入力データ】
            ターゲットキーワード: {{#start.target_keyword#}}
            ビジネス情報: {{#start.business_info#}}
            分析タイプ: {{#start.analysis_type#}}
            
            【API結果】
            {{#google_api_request.text#}}
            
            【分析項目】
            1. キーワード分類（ピラー・クラスター構造）
            2. 優先度ランキング（検索ボリューム・難易度・ビジネス適合性）
            3. 意図分析（情報系・比較系・購買系）
            4. 関連キーワード提案
            5. 実装優先度の理由
            
            【出力形式】
            以下のマークダウン形式で出力：
            # キーワード戦略レポート
            
            ## 推奨キーワード（TOP 10）
            | ランク | キーワード | ボリューム | 難易度 | 意図 | 優先度 |
            |-------|-----------|----------|-------|------|--------|
            
            ## ピラー・クラスター構造
            [構造説明]
            
            ## 実装ロードマップ
            [段階別計画]
        selected: false
        title: キーワード戦略分析
        type: llm
        variables: []
        vision:
          enabled: false
      height: 90
      id: analysis_llm
      position:
        x: 1360
        y: 300
      positionAbsolute:
        x: 1360
        y: 300
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        context:
          enabled: false
          variable_selector: []
        desc: 競合分析を実施（ファイル入力時）
        model:
          completion_params:
            temperature: 0.7
            max_tokens: 1000
          mode: chat
          name: claude-opus-4-1-20250805
          provider: langgenius/anthropic/anthropic
        prompt_template:
        - id: competitor_analysis
          role: user
          text: |
            競合サイトの情報を分析して、差別化キーワード戦略を提案してください。
            
            自社情報: {{#start.business_info#}}
            
            競合情報:
            {{#file_extract.file_content#}}
            
            以下を分析：
            1. 競合が使用しているキーワード
            2. 自社が未カバーのニッチキーワード
            3. 差別化ポイント
            4. 推奨実装キーワード
        selected: false
        title: 競合分析
        type: llm
        variables: []
        vision:
          enabled: false
      height: 90
      id: competitor_analysis_llm
      position:
        x: 1360
        y: 430
      positionAbsolute:
        x: 1360
        y: 430
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        desc: 最終レポートを生成
        selected: false
        template: |
          # SEOキーワード設計レポート
          生成日時: {{#current_time#}}
          
          ## 分析対象
          - ターゲットキーワード: {{#start.target_keyword#}}
          - ビジネス: {{#start.business_info#}}
          - 分析タイプ: {{#start.analysis_type#}}
          
          ## キーワード戦略
          {{#analysis_llm.text#}}
          
          {{#if_condition "competitor_files" "is-not-empty"}}
          ## 競合分析
          {{#competitor_analysis_llm.text#}}
          {{/if_condition}}
          
          ## 次のステップ
          1. 提案されたキーワードについてコンテンツ計画を立案
          2. 優先度の高いキーワードから記事執筆開始
          3. 3ヶ月後に効果測定と戦略調整
        title: レポートフォーマット
        type: template-transform
        variables: []
      height: 90
      id: report_formatter
      position:
        x: 1680
        y: 350
      positionAbsolute:
        x: 1680
        y: 350
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    - data:
        desc: 最終レポートを出力
        outputs:
        - value_selector:
          - report_formatter
          - text
          value_type: string
          variable: seo_keyword_report
        selected: false
        title: 終了
        type: end
      height: 90
      id: end
      position:
        x: 2000
        y: 350
      positionAbsolute:
        x: 2000
        y: 350
      selected: false
      sourcePosition: right
      targetPosition: left
      type: custom
      width: 244
    edges:
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: start
        targetType: if-else
      id: start-condition
      source: start
      sourceHandle: source
      target: input_condition
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: if-else
        targetType: loop
      id: condition-loop
      source: input_condition
      sourceHandle: 'files_only'
      target: file_loop
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: if-else
        targetType: loop
      id: condition-loop-both
      source: input_condition
      sourceHandle: 'both'
      target: file_loop
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: if-else
        targetType: llm
      id: condition-api
      source: input_condition
      sourceHandle: 'text_only'
      target: api_builder_llm
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: true
        loop_id: file_loop
        sourceType: loop-start
        targetType: template-transform
      id: loop-extract
      source: file_loop_start
      sourceHandle: source
      target: file_extract
      targetHandle: target
      type: custom
      zIndex: 1002
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: http-request
      id: builder-api
      source: api_builder_llm
      sourceHandle: source
      target: google_api_request
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: http-request
        targetType: llm
      id: api-analysis
      source: google_api_request
      sourceHandle: source
      target: analysis_llm
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: http-request
        targetType: llm
      id: api-competitor
      source: google_api_request
      sourceHandle: source
      target: competitor_analysis_llm
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: template-transform
      id: analysis-report
      source: analysis_llm
      sourceHandle: source
      target: report_formatter
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: llm
        targetType: template-transform
      id: competitor-report
      source: competitor_analysis_llm
      sourceHandle: source
      target: report_formatter
      targetHandle: target
      type: custom
      zIndex: 0
    - data:
        isInIteration: false
        isInLoop: false
        sourceType: template-transform
        targetType: end
      id: report-end
      source: report_formatter
      sourceHandle: source
      target: end
      targetHandle: target
      type: custom
      zIndex: 0
  viewport:
    x: 106
    y: 11
    zoom: 0.8